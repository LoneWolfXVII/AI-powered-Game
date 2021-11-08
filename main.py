import pygame
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT, BLACK, RED
from checkers.game import Game
from minimax.aiAlgorithm import minimax
from webcolors import rgb_to_name

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CHECKERS w/ AI')

def get_RowColFromMouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        
        if game.turn == RED:
            value, new_board = minimax(game.get_board(), 2, RED, game)
            game.ai_move(new_board)

        if game.winner() != None:
            #isWinner = rgb_to_name(game.winner(), spec='css3')
            isWinner = game.winner()
            print('Winner is: ' + str(isWinner))
            run = False
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_RowColFromMouse(pos)
                if game.turn == BLACK:
                    game.select(row, col)

        game.update()

    pygame.quit()

main()