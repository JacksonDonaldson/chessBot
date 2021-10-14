import discord
import chess
import random

client = discord.Client()
challenges = {}
games = {}
droffers = []

@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    #print("message received")
    if message.author == client.user:
        return

    if message.content.startswith("~help"):
        await botHelp(message)
        return
    
    if message.content.startswith("~challenge"):
        await challenge(message)
        return

    if message.content.startswith("~cancel"):
        await cancel(message)
        return

    
    if message.content.startswith("~accept"):
        await accept(message)
        return
    
    if message.content.startswith("~reject"):
        await reject(message)
        return
    
    if message.content.startswith("~play"):
        await play(message)
        return

    if message.content.startswith("~draw"):
        await draw(message)
        return

    if message.content.startswith("~resign"):
        await resign(message)
        return
    
    
async def botHelp(message):
    await message.channel.send("Available commands: ~challenge (@user), ~play (move), ~accept, ~reject, ~resign, ~draw, ~cancel")

async def challenge(message):
    mentions = message.raw_mentions
    
    if len(mentions) != 1:
        await message.channel.send("Please mention the 1 user you wish to challenge in your message.")
        return
    
    mention = mentions[0]
    user = await client.fetch_user(mention)

    
##        if user == message.author:
##            await message.channel.send("You can't challenge yourself.")
##            return
##        
    if user == client.user:
        await message.channel.send("chessBot challenge functionality not yet set up.")

    #if already an active challenge, don't accept another from same user.
    if message.author.id in challenges.values():
        await message.channel.send("You already have an active challenge. ~cancel to cancel that challenge")
        return

    if user.id in challenges.keys():
        await message.channel.send("Challenged user already has an active challenge")
        return
    
    challenges[user.id] = message.author.id
    await message.channel.send(user.name + ", you have been challenged. ~accept or ~reject.")


async def cancel(message):
    if message.author.id not in challenges.values():
        await message.channel.send("no pending challenges.")
        return
    for key in challenges.keys():
        if challenges[key] == message.author.id:
            challenges.pop(key)
            return
    print("error, cancel failed")

async def accept(message):
    if message.author.id not in challenges.keys():
        await message.channel.send("No pending challenges.")
        return
    challenged = await client.fetch_user(challenges[message.author.id])
    challenges.pop(message.author.id)
    
    await message.channel.send("Match starting between " + message.author.name + " and " + challenged.name)


    if(random.randint(0,1) == 1):
        white = message.author.id
        wn = message.author.name
        black = challenged.id
    else:
        white = challenged.id
        wn = challenged.name
        black = message.author.id

    
    board = chess.Chessboard(white, black)

    games[white] = board
    games[black] = board
    
    moves = str(list(board.findValidMoves("w").keys()))[1:]
    moves = moves[:-1]
    
    board.saveBoardImage()
    image = discord.File("currentBoard.png")
    
    await message.channel.send(file = image, content = wn + ", you're white. Valid moves: " + moves)

async def reject(message):
    if message.author.id not in challenges.keys():
        await message.channel.send("No pending challenges.")
        return
    challenges.pop(message.author.id)
    await message.channel.send("Rejected challenge")

async def play(message):
    if message.author.id in droffers:
        droffers.remove(message.author.id)
    if message.author.id not in games.keys():
        await message.channel.send("No active games. ~challenge someone to start one!")
        return

    board = games[message.author.id]
    if (board.move % 2 == 1 and board.white != message.author.id):
        await message.channel.send("Not your turn!")
        return
    if board.move % 2 == 0 and board.black != message.author.id:
        await message.channel.send("Not your turn!")
        return

    #we know it's somebody with a game, and that it's their turn, so try and play the move they sent
    move = message.content[6:]
    result = board.tryPlayMove(move)
    #result could be w, for white win, b for black win, d for draw, s for successful move, or f for failed move.
    
    if result == "f":
        #failed
        await message.channel.send("Move " + move + " not recognized. Please try again.")
        return
    else:
        #move made
        #other person's turn
        await message.channel.send("Move accepted.")
        board.saveBoardImage()
        file = discord.File("currentBoard.png")

        #redo result to see if it's checkmate or something
        result = board.tryPlayMove(" ")
        if result == "w":
            await message.channel.send(file = file, content = "White wins by checkmate")
            games.pop(board.white)
            games.pop(board.black)
        if result == "b":
            await message.channel.send(file = file, content = "Black wins by checkmate")
            games.pop(board.white)
            games.pop(board.black)
        if result == "d":
            await message.channel.send(file = file, content = "Draw")
            games.pop(board.white)
            games.pop(board.black)
            
        if result == "f":
            if board.move % 2 == 1:
                moves = str(list(board.findValidMoves("w").keys()))[1:]
                nextPlayer = await client.fetch_user(board.white)
                nextPlayer = nextPlayer.name
            else:
                moves = str(list(board.findValidMoves('b').keys()))[1:]
                nextPlayer = await client.fetch_user(board.black)
                nextPlayer = nextPlayer.name
                
            moves = moves[:-1]

            await message.channel.send(file = file, content = nextPlayer + ", you're up. Valid moves: " + moves)


async def draw(message):
    if message.author.id in droffers:
        await message.channel.send("Draw by agreement")
        board = games[message.author.id]
        print(games)
        games.pop(board.white)
        games.pop(board.black)
        print(games)
    else:
        if games[message.author.id].white != message.author.id:
            user = games[message.author.id].white
        else:
            user = games[message.author.id].black
        await message.channel.send("Draw offered. ~draw to accept")
        droffers.append(user)

async def resign(message):
    if message.author.id not in games.keys():
        await message.channel.send("No active games. ~challenge someone to start one!")
        return
    board = games[message.author.id]
    if board.white == message.author.id:
        await message.channel.send("Black wins by resignation")
    elif board.black == message.author.id:
        await message.channel.send("White wins by resignation")
    else:
        print("weird problem with resign")
    games.pop(board.white)
    games.pop(board.black)
    
client.run("ODQ0NTQ4NTE4MzgzNDUyMTcx.YKUBGQ.BAh6ipKV26j_2jaycki7X8HwAKo")        
