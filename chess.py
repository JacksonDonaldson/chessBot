import copy
import numpy
from PIL import Image
#todo:
#nothing?

class ChessPiece:
    def __init__(self, position,color):
        self.position = position
        self.color = color
    def moves(self, board):
        #must be overridden by individual classes
        #returns a list of all the valid moves for that piece, not paying attention to if results in check
        raise Exception("Error: validMoves must be overrided by every ChessPiece child")
    
    def update(self, newPosition, turn):
        self.position = newPosition
    
class Pawn(ChessPiece):
    name = "P"
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.hasMoved = False
        self.canBeEnPassanted = False

    def __str__(self):
        if self.color == "w":
            return "\u2659"
        return "\u265f"

    
    def moves(self, board):
        moveList = []
        if self.color == "w":
            direction = -1
        else:
            direction = 1
        r = self.position[0]
        c = self.position[1]
        if board.exAndNotOc([r + direction, c]):
            #up 1 is valid
            moveList.append([self.position.copy(), [r + direction, c]])
            
            if not self.hasMoved and board.exAndNotOc([r + 2 * direction, c]):
                #up 2 is valid
                moveList.append([self.position.copy(), [r + 2 * direction, c]])


                
        if board.exAndOc([r + direction, c + 1]) and board.board[r + direction][c + 1].color != self.color:
            #taking to +1 is valid
            moveList.append([self.position.copy(), [r + direction,c + 1]])

            
        if board.exAndOc([r + direction, c - 1]) and board.board[r + direction][c - 1].color != self.color:
            #taking to -1 is valid
            moveList.append([self.position.copy(), [r + direction,c - 1]])


            
        #check to left and right for potential en passant
        if board.exAndOc([r, c - 1]) and board.board[r][c - 1].color != self.color:
            if board.board[r][c - 1].name == "P":
                if board.board[r][c - 1].canBeEnPassanted == board.move:
                    #can en passant to -1
                    moveList.append([self.position.copy(), [r + direction,c - 1]])
                    #print("And it's en passantable")
                else:
                    pass
                    #print("en passant failed")
                    #print(board.move)

                
        if board.exAndOc([r, c + 1]) and board.board[r][c + 1].color != self.color:
            if board.board[r][c + 1].name == "P":
                if board.board[r][c + 1].canBeEnPassanted == board.move:
                #can en passant to +1
                    #print("And it's en passantable!")
                    moveList.append([self.position.copy(), [r + direction, c+ 1]])
                else:
                    pass
                    #print("en passant failed")
                    #print(board.move)

                
        return moveList
    def update(self, newPosition, turn):
        if(abs(newPosition[0] - self.position[0])) == 2:
            #we did a double jump
            self.canBeEnPassanted = turn
            #print(turn)
            #print("double jumped")
        else:
            self.canBeEnPassanted = False
        self.position = newPosition
        self.hasMoved = True
    
class Rook(ChessPiece):
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.hasMoved = False
        
    name ="R"
    def __str__(self):
        if self.color == "w":
            return "\u2656"
        return "\u265C"
    def moves(self, board):
        moveList = []
##        r = self.position[0]
##        c = self.position[1]
        for direction in [[1,0],[-1,0],[0,1],[0,-1]]:
            i = 1
            pos = numpy.add(self.position, direction)
            while board.exAndNotOc(pos):
                #this place is a valid space for the rook to move to
                #print(pos)
                #print(direction)
                moveList.append([self.position, list(pos)])
                i +=1
                pos = numpy.add(self.position.copy(), numpy.array(direction) * i)
                
            #check if the last piece is something we can take
            if board.exists(pos) and board.board[pos[0]][pos[1]].color != self.color:
                moveList.append([self.position.copy(), list(pos)])
                
        return moveList
    def update(self, newPosition, turn):
        self.position = newPosition
        self.hasMoved = True
                
class Bishop(ChessPiece):
    name = "B"
    def __str__(self):
        if self.color == "w":
            return "\u2657"
        return "\u265D"
    def moves(self, board):

        moveList = []
##        r = self.position[0]
##        c = self.position[1]
        for direction in [[1,1],[-1,-1],[1,-1],[-1,1]]:
            i = 1
            pos = numpy.add(self.position, direction)
            while board.exAndNotOc(pos):
                #this place is a valid space for the rook to move to
                #print(pos)
                #print(direction)
                moveList.append([self.position, list(pos)])
                i +=1
                pos = numpy.add(self.position.copy(), numpy.array(direction) * i)
                
            #check if the last piece is something we can take
            if board.exists(pos) and board.board[pos[0]][pos[1]].color != self.color:
                moveList.append([self.position.copy(), list(pos)])
                
        return moveList


class Knight(ChessPiece):
    name = "N"
    def __str__(self):
        if self.color == "w":
            return "\u2658"
        return "\u265E"
    def moves(self, board):
        moveList = []
        for direction in [[2,1],[-2,1],[2,-1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]]:
            location = numpy.add(self.position, direction)
            if board.exists(location) and board.occupied(location):
                if board.board[location[0]][location[1]].color != self.color:
                    moveList.append([self.position.copy(), list(location).copy()])
            elif board.exists(location):
                moveList.append([self.position.copy(), list(location).copy()])
        return moveList
class Queen(ChessPiece):
    name = "Q"
    def __str__(self):
        if self.color == "w":
            return "\u2655"
        return "\u265B"
    def moves(self, board):
        moveList = []
##        r = self.position[0]
##        c = self.position[1]
        for direction in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]:
            i = 1
            pos = numpy.add(self.position, direction)
            while board.exAndNotOc(pos):
                #this place is a valid space for the rook to move to
                #print(pos)
                #print(direction)
                moveList.append([self.position, list(pos)])
                i +=1
                pos = numpy.add(self.position.copy(), numpy.array(direction) * i)
                
            #check if the last piece is something we can take
            if board.exists(pos) and board.board[pos[0]][pos[1]].color != self.color:
                moveList.append([self.position.copy(), list(pos)])
                
        return moveList
class King(ChessPiece):
    name = "K"
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.hasMoved = False
        
    def __str__(self):
        if self.color == "w":
            return "\u2654"
        return "\u265A"
    def moves(self, board):
        moveList = []
        for direction in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]:
            location = numpy.add(self.position, direction)
            if board.exists(location) and board.occupied(location):
                if board.board[location[0]][location[1]].color != self.color:
                    moveList.append([self.position.copy(), list(location.copy())])
            elif board.exists(location):
                moveList.append([self.position.copy(), list(location.copy())])

        #todo: castle
        if (not self.hasMoved):
            #potential...
            #check left
            row = self.position[0]
            if board.exAndOc([self.position[0], 0]):
                #check clear to there
                if not board.occupied([row, 1]):
                    if not board.occupied([row, 2]):
                        if not board.occupied([row, 3]):
                            #maybe long castle?
                            if board.board[row][0].name == "R" and not board.board[row][0].hasMoved:
                                #long castle!
                                #(if not in check)

                                #:(
                                board.board[row][1] = self
                                board.board[row][2] = self
                                board.board[row][3] = self
                                if not board.checkCheck(self.color, board):
                                    board.board[row][1] = 0
                                    if not board.checkCheck(self.color, board):
                                        board.board[row][2] = 0
                                        if not board.checkCheck(self.color, board):
                                            board.board[row][3] = 0
                                            if not board.checkCheck(self.color, board):
                                                #long castle!
                                                moveList.append(["0-0-0", "dummy"])
            if board.exAndOc([row, 7]):
                if not board.occupied([row, 6]):
                    if not board.occupied([row, 5]):
                        #maybe short castle?
                        if board.board[row][7].name == "R" and not board.board[row][7].hasMoved:
                            #short castle!
                            #if no check
                            board.board[row][5] = self
                            board.board[row][6] = self
                            if not board.checkCheck(self.color, board):
                                board.board[row][4] = 0
                                if not board.checkCheck(self.color, board):
                                    board.board[row][5] = 0
                                    if not board.checkCheck(self.color, board):
                                        #short castle!
                                        board.board[row][6] = 0
                                        
                                        moveList.append(["0-0", "dummy"])
                            board.board[row][4] = self
                    
                
        return moveList

    def update(self, newPosition, turn):
        self.hasMoved = True
        self.position = newPosition
        
    

    
class Chessboard:
    def __init__(self, white, black, board = None, move = None):
        self.white = white
        self.black = black
        if(board == None):
            self.move = 1
            self.board = [[Rook([0,0],"b"),Knight([0,1],"b"),Bishop([0,2],"b"),Queen([0,3],"b"),King([0,4],"b"),Bishop([0,5],"b"),Knight([0,6],"b"),Rook([0,7],"b")],
                      [Pawn([1,0],"b"),Pawn([1,1],"b"),Pawn([1,2],"b"),Pawn([1,3],"b"),Pawn([1,4],"b"),Pawn([1,5],"b"),Pawn([1,6],"b"),Pawn([1,7],"b")],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [Pawn([6,0],"w"),Pawn([6,1],"w"),Pawn([6,2],"w"),Pawn([6,3],"w"),Pawn([6,4],"w"),Pawn([6,5],"w"),Pawn([6,6],"w"),Pawn([6,7],"w")],
                      [Rook([7,0],"w"),Knight([7,1],"w"),Bishop([7,2],"w"),Queen([7,3],"w"),King([7,4],"w"),Bishop([7,5],"w"),Knight([7,6],"w"),Rook([7,7],"w")]]
            
        else:
            self.board = board
            self.move = move
    def __str__(self):
        #print the board
        text = ""
        for r in self.board:
            text += "| "
            for c in r:
                if c == 0:
                    text += "\u2001 | "
                else:
                    text += str(c) + " | "
            text += "\n" + ("-" * 24) + "\n"
        return text



    def getImage(self, color, name):
        i = Image.open(color + name + ".png")
        o = Image.new(i.mode, (128,128),(0,0,0,0))
        o.paste(i, (int((128 - i.width)/2),128-i.height))
        return o
    def expand(self, ar, x):
        #takes a 2d array and returns a larger one with values repeated x times
        toReturn = []
        for row in ar:
            for i in range(0,x):
                addRow = []
                for element in row:
                    for j in range(0,x):
                        addRow.append(element)
                toReturn.append(addRow.copy())
        return toReturn

    
        
    def saveBoardImage(self):
        #returns a path to an image representing the current board state
        #creates a pixel by pixel representation of the image
##        black = (0, 0, 0)
##        brown = (208, 156, 74, 255)
##        white = (216, 212, 205, 255)
##        image = [[3,0,1,0,1,0,1,0,1],
##         [3,1,0,1,0,1,0,1,0],
##         [3,0,1,0,1,0,1,0,1],
##         [3,1,0,1,0,1,0,1,0],
##         [3,0,1,0,1,0,1,0,1],
##         [3,1,0,1,0,1,0,1,0],
##         [3,0,1,0,1,0,1,0,1],
##         [3,1,0,1,0,1,0,1,0],
##         [3,3,3,3,3,3,3,3,3]]
##        image = self.expand(image, 128)
##        print("expanded")
##        
##        #print out image
##        i = Image.new("RGBA", (128*9,128*9))
##        for x in range(0,len(image)):
##            #print(x)
##            for y in range(0,len(image[x])):
##                if image[x][y] == 0:
##                    color = white
##                elif image[x][y] == 1:
##                    color = brown
##                elif image[x][y] == 3:
##                    color = black
##
##                i.putpixel((len(image) - 1 - x,len(image) - 1 - y), color)
##        print("pixeled")

        if self.move % 2 == 1:
            #print("white side")
            i = Image.open("boardWhite.png")
        else:
            #print("black side")
            i = Image.open("boardBlack.png")
        #put images on board to represent pieces
        for row in self.board:
            for piece in row:
                if piece != 0:
                    pImage = self.getImage(piece.color, piece.name.lower())
                    if(self.move % 2 == 1):
                        i.paste(pImage, (piece.position[1] * 128 + 128, piece.position[0] * 128), pImage)
                    else:
                        i.paste(pImage, ((7-piece.position[1]) * 128 + 128, (7-piece.position[0]) * 128), pImage)
        i.save("currentBoard.png")
        return i
         
    
    def whiteMove(self):
        return input("white move:")
    
    def blackMove(self):
        return input("black move:")
    
    def pieces(self, color,board):
        #returns a list all pieces of one color
        toReturn = []
        for r in board.board:
            for c in r:
                if c !=0 and c.color == color:
                    toReturn.append(c)
        return toReturn

    
    def uncheckedMoves(self, side, board):
        #returns movelist of all possible moves, ignoring checks and such
        uncheckedMoves = []
        if side == "w":
            pieces = self.pieces("w", board)
        else:
            pieces = self.pieces("b", board)
            
        for piece in pieces:
            i = piece.moves(board);
            for j in i:
                uncheckedMoves.append([piece, j[0], j[1]])
        return uncheckedMoves;
    
    def findKingPos(self, side, board):
        #returns the king of a side
        for r in range(0, len(board.board)):
            for c in range(0, len(board.board[r])):
                if board.board[r][c] != 0 and  board.board[r][c].name == "K" and  board.board[r][c].color == side:
                    return [r,c]
        print("error: King of said color not found")
        print("color: " + side)
        print("board: ")
        print(board)

        
    def checkCheck(self, side, board):
        #returns true if side's king can be taken in this position, and false otherwise
        kingPos = board.findKingPos(side, board)
        #print(kingPos)
        if side == "w":
            otherMoves = self.uncheckedMoves("b", board)
        else:
            otherMoves = self.uncheckedMoves("w", board)
        #if any of otherMoves end where the king is at, then the king could be taken
        #print(otherMoves)
        for move in otherMoves:
            #print(type(move[2]))
            #print(move[0])
            if move[1] == "0-0" or move[1] == "0-0-0":
                continue
                #you can't take a piece on a castle, so we ignore it to make this easier
            
            if move[2] == kingPos:
                return True
        return False

    def playMove(self, move):
        board = self.board
        #print(move[3])
        if move[1] != "0-0" and move[1] != "0-0-0":
            piece = board[move[1][0]][move[1][1]]
        self.move +=1
        
        if move[1] == "0-0-0":
            piece = board[move[0].position[0]][4]
            #print("playing castling long!")
            #reset king square
            board[piece.position[0]][piece.position[1]] = 0
            #move king to right square
            board[piece.position[0]][2] = piece
            #update king
            piece.update([piece.position[0], 2], "dummy")
            
            rook = board[piece.position[0]][0]
            #reset rook square
            board[piece.position[0]][0] = 0
            #move rook to new position
            board[piece.position[0]][3] = rook
            #update rook
            rook.update([piece.position[0], 3], "dummy")
            
        elif move[1] == "0-0":
            piece = board[move[0].position[0]][4]
            #print("playing castling short!")
            #reset king square
            board[piece.position[0]][piece.position[1]] = 0
            #move king to right square
            board[piece.position[0]][6] = piece
            #update king
            piece.update([piece.position[0], 6], "dummy")
            
            rook = board[piece.position[0]][7]
            #reset rook square
            board[piece.position[0]][7] = 0
            #move rook to new position
            board[piece.position[0]][5] = rook
            #update rook
            rook.update([piece.position[0], 5], "dummy")
        else:

            
            piece.update(move[2], self.move)
            self.board[move[1][0]][move[1][1]] = 0
            

            if piece.name == "P":
                
                #check for en passant to remove other pawn
                if move[1][1] != move[2][1]:
                    #moving over(capturing)
                    if self.board[move[2][0]][move[2][1]] == 0:
                        #it is en passant
                        print("removing other pawn in wrong spot")
                        self.board[move[1][0]][move[2][1]] = 0

                #deal with promotions
                if "=" in move[3]:
                    print("promoting!")
                    p = move[3][-1]
                    if p == "Q":
                        piece = Queen(move[2].copy(), piece.color)
                    elif p == "R":
                        piece = Rook(move[2].copy(), piece.color)
                    elif p == "B":
                        piece = Bishop(move[2].copy(), piece.color)
                    elif p == "N":
                        piece = Knight(move[2].copy(), piece.color)
                    else:
                        print("pawn selection error!")
                
            self.board[move[2][0]][move[2][1]] = piece

            
    def findValidMoves(self,side):
        #returns a list of all valid moves for side in this position
        if side == "w":
            unchecked = self.uncheckedMoves("w", self)
        else:
            unchecked = self.uncheckedMoves("b", self)

        
        #found list of potentially valid moves. 
        #for each move in uncheckedMoves, check to see if that move would put the side into check- if it would,it's not valid
        #print(self.board[6][0].position)
        checked = []
        for move in unchecked:
            #create a new chessboard with the new positions, and see if it works
            c= Chessboard(0, 1, copy.deepcopy(self.board), self.move)
            move.append("garbage")
            c.playMove(move)            
            #print(c)
            #piece moved to it's next spot- now see if any of the other side's pieces have lineofsight to the king
            if not self.checkCheck(side, c):
                #a valid move
                checked.append(move)
        #print(checked)
        #print(self.board[6][0].position)
        #valid moves found, in terms of position. Now, create a dictionary of AN moves that converts to positional notation
        AN = []
        ANmoves = []
        for move in checked:
            i = self.toAN(move)
            if "=" in i:
                #pawn promotion
                for j in ["N","B","R","Q"]:
                    AN.append(i+j)
                    ANmoves.append(move)
            else:
                #check for conflicts
##                if i in AN:
##                    #Simplest version of AN already exists- we must add starting position delineators
##                    #this is bad, and I think it doesn't properly account for the potential for 3 promotions to Q that are all attacking the same target
##                    #But hopefully that just doesn't happen
##                    #it seems rare enough
##                    otherMove = ANmoves[AN.index(i)]
##                    thisStart = move[1]
##                    otherStart = otherMove[1]
##                    thisStart = self.fileToLetter(thisStart[0]) + str(thisStart[1]+1)
##                    otherStart = self.fileToLetter(otherStart[0]) + str(otherStart[1]+1)
##                    if thisStart[0] == otherStart[0]:
##                        thisStart=thisStart[1]
##                        otherStart = otherStart[1]
##                    elif thisStart[1] == otherStart[1]:
##                        thisStart = thisStart[0]
##                        otherStart = otherStart[0]
##                    AN[AN.index(i)] = AN[AN.index(i)][0:1] + otherStart + AN[AN.index(i)][1:]
##                    i = i[0:1] + thisStart + i[1:]
                    
                AN.append(i)
                ANmoves.append(move)
        #now, check for duplicate moves
        ANdict = {}
        #print(AN)
        for i in range(0,len(AN)):
            if AN[i] not in AN[i+1:]:
                ANdict[AN[i]] = ANmoves[i]
            else:
                #print("conflict found")
                #print(AN[i])
                #we have a conflict...
                #check for the number of others that conflict
                conflicts = [i]
                j = i
                while AN[i] in AN[j+1:]:
                    #print("loop")
                    j = AN[j+1:].index(AN[i]) + j  + 1
                    #print(j)
                    conflicts.append(j)
                #index of all conflicting moves is in conflicts
                #compare each item to each other item to see what's needed to differentiate - 0 for nothing, 1 for file, 2 for rank, 3 for both
                needed = [0] * len(conflicts)
                for j in range(0,len(conflicts)):
                    for k in range(1,len(conflicts)):
                        #check what j and k need to differentiate themselves
                        move1 = ANmoves[conflicts[j]]
                        move2 = ANmoves[conflicts[k]]
                        move1Start = self.fileToLetter(move1[1][1]) + str(8- move1[1][0])
                        move2Start = self.fileToLetter(move2[1][1]) + str(8- move2[1][0])
                        differentiation = 0
                        #position found in file/rank notation. next, determine what's different
                        if (move1Start[0] != move2Start[0]):
                            #files are different. we can just use those
                            differentiation = 1
                        if(move1Start[1] != move2Start[1]):
                            #ranks are different. we can use those
                            differentiation = 2
                        else:
                            #both are the same somehow? tf?
                            print("Error: 2 moves with same start point?")
                            print(move1)
                            print(move2)
                            
                        #add obtained needed differentiation to needed
                        for l in [j,k]:
                            if (needed[l] != 0 and needed[l] != differentiation):
                                needed[l] = 3
                            else:
                                needed[l] = differentiation
                        
                
                #apply differentiation
                #print(needed)
                #print(conflicts)
                for j in conflicts:
                    move = ANmoves[j]
                    moveAN = AN[j]
                    differentiation = needed[conflicts.index(j)]
                    if differentiation == 0:
                        print("Error: no differentiation needed?")
                        print(move)
                        print(moveAN)
                    elif differentiation == 1:
                        moveAN = moveAN[0:1] + self.fileToLetter(move[1][1]) + moveAN[1:]
                    elif differentiation == 2:
                        moveAN = moveAN[0:1] + str(8- move[1][0]) + moveAN[1:]
                    elif differentiation == 3:
                        moveAN = moveAN[0:1] + self.fileToLetter(move[1][1]) + str(8 - move[1][0]) + moveAN[1:]
                    ANdict[moveAN] = move
                    
                    
        return ANdict
            
            

    
    def fileToLetter(self, move):
        #converts a file from positional to letters
        return "abcdefgh"[move]
    
    def toAN(self, move):
        #print(move)
        #converts a move from positional notation (piece, startPosition, endPosition)
        #to Algebraic Notation
        #precondition: move is a valid chess move
        #does not disambiguate moves- this is handled in the function that calls this, which creates a list of all valid moves
        
        piece = move[0]
        startPos = move[1]
        if startPos == "0-0":
            return startPos
        if startPos == "0-0-0":
            return startPos
        startPos = startPos.copy()
        endPos = move[2].copy()
        
        #to do: add special check for long/short castle here
        
        if piece.name != "P":
            AN = piece.name
        else:
            AN = ""
        
        
        capturingEnPassant = False
        if (move[0].name == "P" and move[1][1] != move[2][1]):
            if not self.occupied(endPos):
                #print("en passanting!")
                capturingEnPassant = True
        if(self.occupied(endPos) or capturingEnPassant):
            if AN == "":
                #capturing with pawn- need to add the departing file
                AN = self.fileToLetter(piece.position[1])
            AN+="x"
            #to indicate a capture has taken place

        #add destination square
        AN += self.fileToLetter(endPos[1])
        AN += str(8 - endPos[0])

        #if a pawn moves the the 8th rank, it can promote. In this case, returns the square it moves to and then an equals sign
        #promotion is handled in validMoves
        if(piece.name == "P" and (AN[-1] == "8" or AN[-1] == "1")):
           AN += "="
        #print(AN)
        return AN
        


            
    
    def playNextMove(self):
        
        if self.move%2 == 1:
            validMoves = self.findValidMoves("w")
        else:
            validMoves = self.findValidMoves("b")

        validMovesList = list(validMoves.keys())
        print(validMovesList)
        print(len(validMovesList))
        if len(validMovesList) == 0:
            #there are no valid moves for the side whos turn it is. If in check, lost, if not, draw
            if self.move % 2 == 1:
                if self.checkCheck("w",self):
                    return "b"
                return "d"
                
            else:
                if self.checkCheck("b", self):
                    return "w"
                return "d"
            
            
        attemptedMove = ""
        print(self)
        print("Valid moves:")
        print(validMovesList)
        
        while attemptedMove not in validMovesList:
            if self.move%2 == 1:
                attemptedMove = self.whiteMove();
            else:
                attemptedMove = self.blackMove();

        #valid move found. playing
        move = validMoves[attemptedMove]
        move.append(attemptedMove)
        self.playMove(move)
        
    def tryPlayMove(self, move):
        if self.move%2 == 1:
            validMoves = self.findValidMoves("w")
        else:
            validMoves = self.findValidMoves("b")

        validMovesList = list(validMoves.keys())
        print(validMovesList)
        print(len(validMovesList))
        if len(validMovesList) == 0:
            print("no moves!")
            #there are no valid moves for the side whos turn it is. If in check, lost, if not, draw
            if self.move % 2 == 1:
                if self.checkCheck("w",self):
                    print('returning b')
                    return "b"
                print('returning d')
                return "d"
                
            else:
                if self.checkCheck("b", self):
                    print('returning w')
                    return "w"
                print('returning d')
                return "d"
            
        attemptedMove = move
        if attemptedMove not in validMovesList:
            return "f"

        #valid move found. playing
        move = validMoves[attemptedMove]
        move[3] = attemptedMove
        
        self.playMove(move)

        return "s"

    
    def play(self):
        while True:
            self.saveBoardImage()
            i = self.playNextMove()
            
            if i:
                break
        if i == "w":
            print("white wins")
        elif i == "b":
            print("black wins")
        elif i == "d":
            print("draw")



    def occupied(self, position):
        return self.board[position[0]][position[1]] != 0
    
    def exists(self, position):
        return 0<=position[0] <= 7 and 0<=position[1] <=7
    def exAndNotOc(self, position):
        return self.exists(position) and not self.occupied(position)
    def exAndOc(self, position):
        return self.exists(position) and self.occupied(position)
                
c = Chessboard(0, 1)
