from copy import deepcopy

#Displays a board and all current pieces
def display(state):
    w = 0
    b = 0
    baseBoard = state[BASEBOARD]
    whitePieces = state[WHITEPIECES]
    blackPieces = state[BLACKPIECES]

    for i in range(len(baseBoard)):
        for j in range(len(baseBoard[0])):
            if w < len(whitePieces):
                if whitePieces[w] == [i,j,K,WHITE]:
                    print(" WK"," ",end="")
                    w+=1
                    continue
                elif whitePieces[w] == [i,j,P,WHITE]:
                    print(" w","  ",end="")
                    w+=1
                    continue
            if b < len(blackPieces):
                if blackPieces[b] == [i,j,K,BLACK]:
                    print(" BK","  ",end="")
                    b+=1
                    continue
                elif blackPieces[b] == [i,j,P,BLACK]:
                    print(" b","  ",end="")
                    b+=1
                    continue
            if baseBoard[i][j] == BLACK:
                print(" #","  ",end="")
            else:
                print(" -","  ",end="")
        print("\n")
        
def isValid(piece):
    if piece[ROW] < 0 or piece[ROW] >= n:
        return False
    if piece[COL] < 0 or piece[COL] >= n:
        return False
    return True


def getLeftMoves(piece):
    moves = None
    newPiece = [piece[ROW]+1,piece[COL]-1,piece[TYPE]]
    if isValid(newPiece):
        moves.append[newPiece]
    if piece[TYPE] == K:
        newPiece = [piece[ROW]-1,piece[COL]-1,piece[TYPE]]
    pass

def getRightMoves(piece):
    pass

def getMoves(piece):
    return getLeftMoves(piece)+getRightMoves(piece)

#Get all possile moves that could be made in a given state
def getChildren(node,maxPlayer):
    children = []
    currentPlayer = None
    otherPlayer = None
    if maxPlayer == True:
        currentPlayer = node[BLACKPIECES]
        otherPlayer = node[WHITEPIECES]
    else:
        currentPlayer = node[WHITEPIECES]
        otherPlayer = node[BLACKPIECES]

    for piece in currentPlayer:
        children.append[getMoves(piece,otherPlayer)]


#Get the heuristic value of a given state
def heuristic(node):
    pass

#Minimax algorithm for computer computer player
#since checkers is a zero-sum game, the max player's
#cost is equal to the negation of the min player's cost
def miniMax(node, depth, maxPlayer, h):
    if depth == 0 or getChildren(node) is None:
        return h(node[0]),node

    bestMove = None
    if maxPlayer == True:
        bestValue = -10000000000
        for child in getChildren(node):
            v = miniMax(child,depth-1,False)
            bestValue = max(bestValue,v)
            bestMove = child
        return bestValue, bestMove
    else:
        bestValue = 10000000000
        for child in getChildren(node):
            v = miniMax(child,depth-1,False)
            bestValue = min(bestValue,v)
            bestMove = child
        return bestValue, bestMove


#Board Size
n = 8
ROW = 0
COL = 1
TYPE = 2
COLOR = 3

BLACK = 0
WHITE = 1
#Value representing a piece as a pawn
P = 1

#Value representing a piece as a king
K = 2

#Index values for a state
BASEBOARD = 0
WHITEPIECES = 1
BLACKPIECES = 2

#Main Board - white = -, black = #
baseBoard = [[ (row+col) % 2 for row in range(n)] for col in range(n)]

#Pieces arrays for each player; white locations are hardcoded, black locations
#are the opposite of the white locations initially
whitePieces = [[0,0,P,WHITE],[0,2,P,WHITE],[0,4,P,WHITE],[0,6,P,WHITE],
               [1,1,P,WHITE],[1,3,P,WHITE],[1,5,P,WHITE],[1,7,P,WHITE],
               [2,0,P,WHITE],[2,2,P,WHITE],[2,4,P,WHITE],[2,6,P,WHITE]]

blackPieces = sorted(list(map(lambda x: [n-x[ROW]-1,n-x[COL]-1,P,BLACK],whitePieces )))

initialState = [baseBoard, whitePieces, blackPieces]

#Display the initial board
# display(initialState)


class Piece:
    def __init__(self, color, i, j):
        self.i = i
        self.j = j
        self.color = color
        self.king = False
    def kingMe(self):
        self.king = True
    def __str__(self):
        return self.color
    def opposite(self, compare):
        if isinstance(compare,Piece):
            return self.color != compare.color
        return False
    def __eq__(self, other):
        if isinstance(other,Piece):
            return self.i == other.i and self.j == other.j
        return False

class Board:
    def __init__(self):
        n = 8
        self.baseBoard = []
        self.whitePieces = []
        self.blackPieces = []
        for i in range(n):
            self.baseBoard.append(['-'] * n)
            for j in range(n):
                if (i+j) % 2 == 1 and len(self.whitePieces) < 12:
                    self.baseBoard[i][j] = Piece('W',i,j)
                    self.whitePieces.append(self.baseBoard[i][j])
                if (n-i) < 4 and (i+j) % 2 == 1:
                    self.baseBoard[i][j] = Piece('B',i,j)
                    self.blackPieces.append(self.baseBoard[i][j])

    def display(self):
        for i in range(len(self.baseBoard)):
            for j in range(len(self.baseBoard[i])):
                print(self.baseBoard[i][j], end="")
                print(" ", end='')
            print('')
        print('\n')

    def getChildren(self, piece):
        moves = []
        return self.findMoves(self,piece)

    def findMoves(self,piece):
        moves = []
        if piece.color == 'W' or piece.king:
            moves += self.nextBoard(piece,1,1)
            moves += self.nextBoard(piece,1,-1)
        if piece.color == 'B' or piece.king:
            moves += self.nextBoard(piece,-1,1)
            moves += self.nextBoard(piece,-1,-1)
        return moves

    def nextBoard(self,piece,i,j):
        newI = piece.i + i
        newJ = piece.j + j
        if newI>7 or newI<0 or newJ>7 or newJ<0:
            return []
        if self.baseBoard[newI][newJ] == '-':
            clone = deepcopy(self)
            arr = clone.whitePieces if piece.color == 'W' else clone.blackPieces
            index = arr.index(piece)
            p = arr[index]
            clone.move(p,newI,newJ)
            return [clone]
        if self.validAttack(piece,i,j):
            clone = deepcopy(self)
            arr = clone.whitePieces if piece.color == 'W' else clone.blackPieces
            index = arr.index(piece)
            p = arr[index]
            clone.attack(p,i,j)
            while(clone.validAttack(p, i, j)):
                clone.attack(p,i,j)
            return [clone]
        else:
            return []
    def attack (self,piece,i,j):
        deli = piece.i + i
        delj = piece.j + j
        self.move(piece,piece.i+i*2,piece.j+j*2)
        arr = self.whitePieces if piece.color == 'B' else self.blackPieces
        index = arr.index(self.baseBoard[deli][delj])
        self.baseBoard[deli][delj] = '-'
        del arr[index]

    def validAttack(self,piece,i,j):
        newI = piece.i + i
        newJ = piece.j + j
        if newI>7 or newI<0 or newJ>7 or newJ<0:
            return False
        if piece.opposite(self.baseBoard[piece.i + i][piece.j + j]):
            return self.baseBoard[piece.i + (i*2)][piece.j + (j*2)] == '-'
        return False
    def move(self,piece,i,j):
        self.baseBoard[piece.i][piece.j], self.baseBoard[i][j] = self.baseBoard[i][j], self.baseBoard[piece.i][piece.j]
        piece.i = i
        piece.j = j
        



test = Board()
test.display()
# print(test.whitePieces)
# print(test.blackPieces)

# test.display()
# print(test.whitePieces[0].opposite(test.blackPieces[0]))

# print(test.whitePieces[0].opposite(test.whitePieces[0]))
white = test.whitePieces[10]
black = test.blackPieces[0]
test.move(white,3,4)
test.move(black,4,3)
test.move(test.blackPieces[8],6,0)
test.move(test.blackPieces[1],5,0)
test.display()

moves = test.nextBoard(white,1,-1)
for move in moves:
    move.display()
# test.display()
# test.display()
# moves = test.getChildren(test.whitePieces[10])
# for move in moves:
#     print("\n")
#     move.display()





