import pygame

class Button:
    def __init__ (self, x, y, width, height, text=None, color=(73,73,73), highlightColor=(189,189,189), function=None, params=None):
        self.image = pygame.Surface((width, height))
        self.pos = (x,y)
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.color = color
        self.highlightColor = highlightColor
        self.function = function
        self.params = params
        self.highlight = False
        self.text = text

    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlight = True
        else:
            self.highlight = False
    
    def draw(self, window):
        if self.highlight:
            self.image.fill(self.highlightColor)
        else:
            self.image.fill(self.color)
        if self.text:
            self.drawText(self.text)
        window.blit(self.image, self.pos)

    def click(self):
        if self.params:
            self.function(self.params)
        else:
            self.function()
     
    def drawText(self, text): 
        font = pygame.font.SysFont("cambria", 20)
        text = font.render(text, False, (0,0,0))
        width, height = text.get_size()
        x = (self.width-width)//2
        y = (self.height-height)//2
        self.image.blit(text, (x, y))
