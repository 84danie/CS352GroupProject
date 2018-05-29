from copy import deepcopy
import tkinter as tk

#Get the heuristic value of a given state
def earlyGameHeuristic(node):
    v = 0
    for piece in node.whitePieces:
        v = v + 10 if piece.king else v + 5
        v = v + 2 if not piece.king and piece.i < 4 else v
    for piece in node.blackPieces:
        v = v - 10 if piece.king else v - 5
        v = v - 2 if not piece.king and piece.i > 5 else v
    return v

def heuristic(node):
    return earlyGameHeuristic(node)

#Minimax algorithm for computer computer player
#since checkers is a zero-sum game, the max player's
#cost is equal to the negation of the min player's cost
def miniMax(node, depth, maxPlayer, h):
    if depth == 0 or not node.getChildren():
        return h(node),node
    bestMove = None
    if maxPlayer == True:
        bestValue = -10000000000
        for child in node.getChildren("W"):
            (newVal, move) = miniMax(child,depth-1,False,h)
            if newVal > bestValue:
                bestValue = newVal
                bestMove = child
        return bestValue, bestMove
    else:
        bestValue = 10000000000
        for child in node.getChildren():
            (newVal, move) = miniMax(child,depth-1,True,h)
            if newVal < bestValue:
                bestValue = newVal
                bestMove = child
        return bestValue, bestMove

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

    def getChildren(self, which="W"):
        moves = []
        if which == "W":
            for piece in self.whitePieces:
                moves += self.findMoves(piece)
        else:
            for piece in self.blackPieces:
                moves += self.findMoves(piece)
        return moves

    def findMoves(self,piece):
        moves = []
        if piece.color == 'W' or piece.king:
            moves += self.nextBoard(piece,1,1)
            moves += self.nextBoard(piece,1,-1)
        if piece.color == 'B' or piece.king:
            moves += self.nextBoard(piece,-1,1)
            moves += self.nextBoard(piece,-1,-1)
        return moves

    def nextBoard(self,piece,i,j, jumped=False):
        newI = piece.i + i
        newJ = piece.j + j
        if newI>7 or newI<0 or newJ>7 or newJ<0:
            return []
        clone = deepcopy(self)
        arr = clone.whitePieces if piece.color == 'W' else clone.blackPieces
        index = arr.index(piece)
        p = arr[index]
        if self.validAttack(piece,i,j):
            if p.king:
                clone.attack(p,i,j)
                moves = []
                for pair in [[1,-1],[1,1],[-1,-1],[-1,1]]:
                    moves += clone.nextBoard(p,pair[0],pair[1], jumped=True)
                if(len(moves)==0):
                    moves.append(clone)
                return moves
            else:
                clone.attack(p,i,j)
                while(clone.validAttack(p, i, j)):
                    clone.attack(p,i,j)
            return [clone]
        if self.baseBoard[newI][newJ] == '-' and not jumped:
            clone.move(p,newI,newJ)
            return [clone]
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
        newI = piece.i + i*2
        newJ = piece.j + j*2
        if newI>7 or newI<0 or newJ>7 or newJ<0:
            return False
        if piece.opposite(self.baseBoard[piece.i + i][piece.j + j]):
            return self.baseBoard[piece.i + (i*2)][piece.j + (j*2)] == '-'
        return False
    
    def move(self,piece,i,j):
        self.baseBoard[piece.i][piece.j], self.baseBoard[i][j] = self.baseBoard[i][j], self.baseBoard[piece.i][piece.j]
        piece.i = i
        piece.j = j
        if piece.color == 'W' and i == 7:
            piece.kingMe()
        if piece.color == 'B' and i == 0:
            piece.kingMe()

class UI(tk.Frame):
    master = tk.Tk()
    chosen = None
    marked = None
    midCombo = False
    
    
    def __init__(self, board, master=None):
       tk.Frame.__init__(self, master)
       self.board = board
       self._btn_matrix = []
       self._sts_matrix = [[0 for x in range(8)] for y in range(8)]
       self.grid()

    def checkForCombo(self):
        if(self.board.baseBoard[UI.chosen[0]][UI.chosen[1]].king):
            if(self.board.validAttack(self.board.baseBoard[UI.chosen[0]][UI.chosen[1]],-1,-1) or self.board.validAttack(self.board.baseBoard[UI.chosen[0]][UI.chosen[1]],-1,1)
               or self.board.validAttack(self.board.baseBoard[UI.chosen[0]][UI.chosen[1]],1,-1) or self.board.validAttack(self.board.baseBoard[UI.chosen[0]][UI.chosen[1]],1,1)):
                return True
            else:
                return False
        else:
            if(self.board.validAttack(self.board.baseBoard[UI.chosen[0]][UI.chosen[1]],-1,-1) or self.board.validAttack(self.board.baseBoard[UI.chosen[0]][UI.chosen[1]],-1,1)):
                return True
            else:
                return False

    #def refreshStates(self):
        

    def markThis(self, row, column):
        print("got here")
        if(UI.chosen == None):
            print("ui chosen is none")
            if(isinstance(self.board.baseBoard[row][column], Piece)):
                print(self.board.baseBoard[row][column].color)
            else:
                print(self.board.baseBoard[row][column])
        else:
            dy = abs(UI.chosen[0] - row)
            dx = abs(UI.chosen[1] - column)
            print("dx ", dx, "dy ",dy)
            if(dy == 1 and dx == 1): 
                self._btn_matrix[UI.chosen[0]][UI.chosen[1]].config(relief='raised')
                if(isinstance(self.board.baseBoard[UI.chosen[0]][UI.chosen[1]], Piece)):
                    i = row - UI.chosen[0]
                    j = column - UI.chosen[1]
                    states = self.board.nextBoard(self.board.baseBoard[UI.chosen[0]][UI.chosen[1]], i, j)
                    if not states:
                        return
                    self.board = states[0]
                    self.refreshGraphics()
                    (val, nextBoard) = miniMax(self.board, 3, True, heuristic)
                    self.board = nextBoard
                    self.refreshGraphics()

        
    def selectThis(self, row, column):
        if(UI.chosen == None):
            UI.chosen = [row, column]
            self._btn_matrix[row][column].config(relief='sunken')
            print("Player piece selected: "+ str(UI.chosen[0]) + " " + str(UI.chosen[1]))
        elif(UI.midCombo is False):
            self._btn_matrix[UI.chosen[0]][UI.chosen[1]].config(relief='raised')
            UI.chosen = [row, column]
            self._btn_matrix[row][column].config(relief='sunken')
            print("New piece selected, changing focus to: " + str(UI.chosen[0]) + " " + str(UI.chosen[1]))

    def createWidgets(self):
        blackPiece = tk.PhotoImage(file="black.gif")
        redPiece = tk.PhotoImage(file="red.gif")
        emptySpot = tk.PhotoImage(file = "empty.gif")
        emptySpot2 = tk.PhotoImage(file = "empty2.gif")
        for x in range(8):
            row_matrix = []
            for y in range(8):
                if(isinstance(self.board.baseBoard[x][y], Piece)):
                    if(self.board.baseBoard[x][y].color == "B"):
                        quitButton = tk.Button(self, image = blackPiece, command=lambda row=x, column=y: self.selectThis(row, column))
                        quitButton.image = blackPiece
                    else:
                        quitButton = tk.Button(self, image = redPiece, command=lambda row=x, column=y: self.markThis(row, column))
                        quitButton.image = redPiece
                else:
                    if(x % 2 == 0):
                        if(y % 2 == 0):
                            quitButton = tk.Button(self, image = emptySpot2, command=lambda row=x, column=y: self.markThis(row, column))
                            quitButton.image = emptySpot2
                        else:
                            quitButton = tk.Button(self, image = emptySpot, command=lambda row=x, column=y: self.markThis(row, column))
                            quitButton.image = emptySpot
                    else:
                        if(y % 2 == 0):
                            quitButton = tk.Button(self, image = emptySpot, command=lambda row=x, column=y: self.markThis(row, column))
                            quitButton.image = emptySpot
                        else:
                            quitButton = tk.Button(self, image = emptySpot2, command=lambda row=x, column=y: self.markThis(row, column))
                            quitButton.image = emptySpot2

                row_matrix.append(quitButton)
                quitButton.grid(row=x, column=y, sticky="wens")
            self._btn_matrix.append(row_matrix)

    def refreshGraphics(self):
        blackPiece = tk.PhotoImage(file="black.gif")
        redPiece = tk.PhotoImage(file="red.gif")
        emptySpot = tk.PhotoImage(file = "empty.gif")
        emptySpot2 = tk.PhotoImage(file = "empty2.gif")
        bKing = tk.PhotoImage(file="blackKing.gif")
        rKing = tk.PhotoImage(file="redKing.gif")
        for x in range(8):
            for y in range(8):
                if(isinstance(self.board.baseBoard[x][y], Piece)):
                    if(self.board.baseBoard[x][y].color == "B"):
                        if(self.board.baseBoard[x][y].king):
                            self._btn_matrix[x][y].configure(image = bKing, command=lambda row=x, column=y: self.selectThis(row, column))
                            self._btn_matrix[x][y].image = bKing
                        else:
                            self._btn_matrix[x][y].configure(image = blackPiece, command=lambda row=x, column=y: self.selectThis(row, column))
                            self._btn_matrix[x][y].image = blackPiece
                    else:
                        if(self.board.baseBoard[x][y].king):
                            self._btn_matrix[x][y].configure(image = rKing, command=lambda row=x, column=y: self.markThis(row, column))
                            self._btn_matrix[x][y].image = rKing
                        else:
                            self._btn_matrix[x][y].configure(image = redPiece, command=lambda row=x, column=y: self.markThis(row, column))
                            self._btn_matrix[x][y].image = redPiece
                else:
                    if(x % 2 == 0):
                        if(y % 2 == 0):
                            self._btn_matrix[x][y].configure(image = emptySpot2, command=lambda row=x, column=y: self.markThis(row, column))
                            self._btn_matrix[x][y].image = emptySpot2
                        else:
                            self._btn_matrix[x][y].configure(image = emptySpot, command=lambda row=x, column=y: self.markThis(row, column))
                            self._btn_matrix[x][y].image = emptySpot
                    else:
                        if(y % 2 == 0):
                            self._btn_matrix[x][y].configure(image = emptySpot, command=lambda row=x, column=y: self.markThis(row, column))
                            self._btn_matrix[x][y].image = emptySpot
                        else:
                            self._btn_matrix[x][y].configure(image = emptySpot2, command=lambda row=x, column=y: self.markThis(row, column))
                            self._btn_matrix[x][y].image = emptySpot2
    


b = Board()
gui = UI(b)
gui.master.title('Checkers')
gui.createWidgets()
gui.mainloop()