import pygame
import sys
from solver import* 
from config import*
from button import*

class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = generateBoard()
        self.selected = None
        self.mousePosition = None
        self.state = "running"
        self.completed = False
        self.cellChanged = False

        self.incorrectCells = []
        self.runningButtons = []
        self.defaultCells = []
        self.font = pygame.font.SysFont("arial", cellSize//2)
        self.load()

    def generate(self):
        self.grid = generateBoard()
        self.load()
        pygame.quit()
        App().run()

    def solveBoard(self):
        toSolve = self.grid
        solve(self.grid)
        self.grid = toSolve

    def run(self):
        while self.running:
            if self.state == "running":
                self.running_events()
                self.running_update()
                self.running_draw()
        pygame.quit()
        sys.exit()

    def running_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.checkOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.runningButtons:
                        if button.highlight:
                            button.click()
            
            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.defaultCells:
                    if (event.unicode).isdigit():
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cellChanged = True

    def running_update(self):
        self.mousePosition = pygame.mouse.get_pos()
        for i in self.runningButtons:
            i.update(self.mousePosition)

        if self.cellChanged:
            self.incorrectCells = []
            if self.allCellsFilled():
                self.checkAllCells()
                if len(self.incorrectCells) == 0:
                    self.completed = True                

    def running_draw(self):
        self.window.fill(WHITE)
        for i in self.runningButtons:
            i.draw(self.window)
        if self.selected:
            self.highlightSelection(self.window, self.selected)

        self.highlightDefaultCells(self.window, self.defaultCells)
        self.highlightIncorrectCells(self.window, self.incorrectCells)
        
        self.drawNumbers(self.window)
        self.drawGrid(self.window)
        pygame.display.update()
        self.cellChanged = False

    def drawGrid(self, window):
        pygame.draw.rect(window, BLACK, (gridPosition[0], gridPosition[1], WIDTH-150, HEIGHT-150),2)
        for x in range(9):
            if x%3 != 0:
                pygame.draw.line(window, BLACK, (gridPosition[0]+(x*cellSize), gridPosition[1]), (gridPosition[0]+(x*cellSize), gridPosition[1]+450))
                pygame.draw.line(window, BLACK, (gridPosition[0], gridPosition[1]+(x*cellSize)), (gridPosition[0]+450, gridPosition[1]+(x*cellSize)))
            else:
                pygame.draw.line(window, BLACK, (gridPosition[0]+(x*cellSize), gridPosition[1]), (gridPosition[0]+(x*cellSize), gridPosition[1]+450), 2)
                pygame.draw.line(window, BLACK, (gridPosition[0], gridPosition[1]+(x*cellSize)), (gridPosition[0]+450, gridPosition[1]+(x*cellSize)), 2)

    
    def checkOnGrid(self):
        if self.mousePosition[0] < gridPosition[0] or self.mousePosition[1] < gridPosition[1]:
            return False
        if self.mousePosition[0] > gridPosition[0]+gridSize or self.mousePosition[1] > gridPosition[1]+gridSize:
            return False
        return ((self.mousePosition[0]-gridPosition[0])//cellSize, (self.mousePosition[1]-gridPosition[1])//cellSize)

    def highlightSelection(self, window, pos):
        pygame.draw.rect(window, LIGHTBLUE, ((pos[0]*cellSize)+gridPosition[0], (pos[1]*cellSize)+gridPosition[1], cellSize, cellSize))

    def loadButtons(self):
        self.runningButtons.append(Button(  75, 40, WIDTH//7, 40,
                                            function=self.checkAllCells,
                                            color=(27,142,207),
                                            text="Check"))
        self.runningButtons.append(Button(  (WIDTH//2-(WIDTH//7)//2)-10, 40, WIDTH//7+20, 40,
                                            color=(117,172,112),
                                            function=self.generate,
                                            params=None,
                                            text="New Game"))
        self.runningButtons.append(Button(  440, 40, WIDTH//7, 40,
                                            color=(199,129,48),
                                            function=self.solveBoard,
                                            params=None,
                                            text="Solve"))

    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize-fontWidth)//2
        pos[1] += (cellSize-fontHeight)//2
        window.blit(font, pos)

    def drawNumbers(self, window):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]!=0:
                    pos = [(j*cellSize)+gridPosition[0], (i*cellSize)+gridPosition[1]]
                    self.textToScreen(window, str(self.grid[i][j]), pos)
    
    def load(self):
        self.loadButtons()
        self.defaultCells = []
        self.incorrectCells = []
        self.completed = False

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]!=0:
                    self.defaultCells.append([j, i])

    def highlightDefaultCells(self, window, default):
        for i in default:
            pygame.draw.rect(window, GREY, (i[0]*cellSize+gridPosition[0], i[1]*cellSize+gridPosition[1], cellSize, cellSize))
    
    def highlightIncorrectCells(self, window, incorrect):
        for i in incorrect:
            pygame.draw.rect(window, RED, (i[0]*cellSize+gridPosition[0], i[1]*cellSize+gridPosition[1], cellSize, cellSize))

    def allCellsFilled(self):
        for i in self.grid:
            for j in i:
                if j == 0:
                    return False
        return True

    def checkAllCells(self):
        self.checkRows()
        self.checkColumns()
        self.checkSmallGrid()

    def checkRows(self):
        for i in range(len(self.grid)):
            possibles = [1,2,3,4,5,6,7,8,9]
            for j in range(len(self.grid[i])):
                if self.grid[i][j] in possibles:
                    possibles.remove(self.grid[i][j])
                else:
                    if [j, i] not in self.defaultCells and [j,i] not in self.incorrectCells:
                        self.incorrectCells.append([j, i])
    
    def checkColumns(self):
        for xidx in range(9):
            possibles = [1,2,3,4,5,6,7,8,9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.defaultCells and [xidx, yidx] not in self.incorrectCells:
                        self.incorrectCells.append([xidx, yidx])
                    if [xidx, yidx] in self.defaultCells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx, k] not in self.defaultCells:
                                self.incorrectCells.append([xidx, k])

    def checkSmallGrid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1,2,3,4,5,6,7,8,9]
                for i in range(3):
                    for j in range(3):
                        xidx = x*3+i
                        yidx = y*3+j
                        if self.grid[yidx][xidx] in possibles:
                            possibles.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.defaultCells and [xidx, yidx] not in self.incorrectCells:
                                self.incorrectCells.append([xidx, yidx])
                            if [xidx, yidx] in self.defaultCells:
                                for k in range(3):
                                    for l in range(3): 
                                        xidx2 = x*3+k
                                        yidx2 = y*3+l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2, yidx2] not in self.defaultCells:
                                            self.incorrectCells.append([xidx2, yidx2]) 

if __name__ == "__main__":
    App().run()
