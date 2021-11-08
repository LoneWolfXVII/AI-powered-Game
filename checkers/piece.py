import pygame
from .constants import COLS, RED, BLACK, SQUARE_SIZE, GREY, CROWN

class Piece:
    PADDING = 13 
    BORDER_OUTLINE = 2 # pixel difference b/w the 2 circles
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False # king peices are those that can jump backwards as well
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 # middle of the squares to make circular pieces
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win): #draw the pieces
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y),
                            radius + self.BORDER_OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y),
                            radius)
        if self.king:
            # blit => put some surface into the screen
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()


    # what is the internal representation of the object
    # debugging ko lai
    def __repr__(self):  
        return str(self.color)      
