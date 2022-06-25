import numpy as np
from config import*
import time 
from read_boards import boardList

def checkConstrains(board: list, row: int, col: int) -> list:
    possibles = [1,2,3,4,5,6,7,8,9]
    for i in range(9):
        if board[row][i] in possibles:
            possibles.remove(board[row][i])

    for i in range(9):
        if board[i][col] in possibles:
            possibles.remove(board[i][col])

    x = (row//3)*3
    y = (col//3)*3
    for i in range(3):
        for j in range(3):
            if board[x+i][y+j] in possibles:
                possibles.remove(board[x+i][y+j])
    
    return possibles

def findEmptyCell(board: list) -> tuple:
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return (row, column)

    return (-100, -100)

def solve(board: list) -> bool:
    row = findEmptyCell(board)[0]
    column = findEmptyCell(board)[1]
    if row == -100 or column == -100:
        return True
        
    possibles = checkConstrains(board, row, column)
    for attempt in possibles:
        board[row][column] = attempt
        if solve(board):
            return True
    board[row][column] = 0
    
    return False


#SOLVE GAMEBOARD
toSolve = []


#SOLVE 50 BOARDS    
# start = time.time()
# count=1
# for b in boardList:
#     print(f'board #{count}\n{np.matrix(b)}')
#     board = b
#     solve(board)
#     print(f'solution:\n{np.matrix(board)}\n')
#     count+=1
# end = time.time()
# print(f'{end-start} seconds')





