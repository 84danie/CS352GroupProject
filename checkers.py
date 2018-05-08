#Displays a board and all current pieces
def displayBoard(baseBoard, whitePieces, blackPieces):
    w = 0
    b = 0
    for i in range(len(baseBoard)):
        for j in range(len(baseBoard[0])):
            if w < len(whitePieces):
                if whitePieces[w] == [i,j]:
                    print("W","  ",end="")
                    w+=1
                    continue
            if b < len(blackPieces):
                if blackPieces[b] == [i,j]:
                    print("B","  ",end="")
                    b+=1
                    continue
            if baseBoard[i][j] == 0:
                print("#","  ",end="")
            else:
                print("-","  ",end="")
        print("\n")

#Board Size
n = 8

#Main Board - white = -, black = #
baseBoard = [[ (row+col) % 2 for row in range(n)] for col in range(n)]

#Pieces arrays for each player; white locations are hardcoded, black locations
#are the opposite of the white locations initially
whitePieces = [[0,0],[0,2],[0,4],[0,6],
               [1,1],[1,3],[1,5],[1,7],
               [2,0],[2,2],[2,4],[2,6]]

blackPieces = sorted(list(map(lambda x: [n-x[0]-1,n-x[1]-1],whitePieces )))

#Display the initial board
displayBoard(baseBoard,whitePieces,blackPieces)
