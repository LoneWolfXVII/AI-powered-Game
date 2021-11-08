# copy -> shallow copy; board references only
# deepcopy -> board with all the references

# x = []
# y = x
# x[0] = 1 ; modifies y as well. Which we don't want

# x = []
# y = deepcopy(x) ; does not modify each other
from copy import deepcopy
import pygame
from pygame import display

RED = (128, 0, 0)
BLACK = (23, 22, 22)

def minimax(position, depth, max_player, game):
    # position -> current pos; board object
    # depth -> how far the tree is extended, we'll decrement by 1 everytime
    # max_player -> boolean; minimizing or maximizing the value
    # game -> game object from main()
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, False, game)[0] # just the value
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth-1, True, game)[0] # just the value
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1]) # moving the piece to that row and column
    if skip:
        board.remove(skip)

    return board

def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_allPieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves

def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,200,0), (piece.x, piece.y), 30, 5)
    game.draw_validMoves(valid_moves.keys())  # {(4,5): [Piece()]}; keys => actual row, col
    pygame.display.update()
    pygame.time.delay(60)