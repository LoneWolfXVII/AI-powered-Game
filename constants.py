import pygame

WIDTH, HEIGHT = 650, 650
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

RED = (128, 0, 0)
BROWN = (178, 117, 55)
WHITE = (255,248,220)
BLACK = (23, 22, 22)
BLUE = (65, 105, 225)
GREY = (160, 160, 160)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (24,12))
