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
        c
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
display(initialState)
