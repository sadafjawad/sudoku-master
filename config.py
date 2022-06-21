from read_boards import boardList
import random

#config
HEIGHT=600
WIDTH=600

gridPosition = (75,100)
cellSize = 50
gridSize = cellSize*9

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (200,200,200)
RED = (200,120,120)
LIGHTBLUE = (96, 216, 232)

#sudoku grid generator
BOARD = [[0 for i in range(9)] for j in range(9)]
def generateBoard():
    BOARD = boardList[random.randint(0,49)]
    return BOARD 

