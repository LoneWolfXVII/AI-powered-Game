import pygame
from .constants import BROWN, COLS, ROWS, WHITE, SQUARE_SIZE, RED, BLACK
from .piece import Piece

## board 
# red = white
# black = brown
# blue = blue

## goti haru
# white = red
# red = black

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.black_left = 12 #no. of pieces
        self.red_kings = self.black_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):  #odd even pattern
                pygame.draw.rect(win, WHITE, 
                        (row*SQUARE_SIZE, 
                        col*SQUARE_SIZE, 
                        SQUARE_SIZE,
                        SQUARE_SIZE)
                    )

    def evaluate(self): # TODO: print final score to console as well ????
        return self.red_left - self.black_left + (self.red_kings * 0.5 - self.red_kings * 0.5)

    def get_allPieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        # swap piece positions
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]  
        piece.move(row, col)

        # check row col to make a piece a king
        if row == ROWS-1 or row == 0:
            piece.make_king()
            if piece.color == RED:
                self.red_kings += 1
            else:
                self.black_kings += 1
    
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            # interior list so as to what each row will have
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row+1) % 2):
                    if row < 3: # 0, 1, 2
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4: # 5, 6, 7
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0) # 0 red or black piece
                else: 
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.red_left -= 1
    
    def winner(self):
        if self.black_left <= 0:
            return RED
        elif self.red_left <= 0:
            return BLACK
        
        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            # (row-1) -> move upwards 
            # max(row-3, -1)
                # row-3 -> move up to 2 squares ATM
                # -1 -> 0th row 
            # (step = -1) -> move up when we incr/decr for loop
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right))

        if piece.color == RED or piece.king:
            # (row+1) -> move downwards 
            # max(row+3, 1)
                # row+3 -> move down to 2 squares ATM
                # ROWS -> 7th row (last)
            # (step = 1) -> move down when we incr/decr for loop
            moves.update(self._traverse_left(row+1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row+1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    # returns a dictionary
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        # start, stop, step => for loops
        # step => up or down while traversing the  (top left/right or bottom left/right diagonal)
        # skipped => if any pieces is skipped yet
        # left => starting column to traverse
        moves = {}
        last = []
        for r in range(start, stop, step): # what row we are starting and stopping by and by what step
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0: # empty square
                if skipped and not last:
                    break
                elif skipped: # double jumping ?
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
                 
            elif current.color == color: # if same color piece is there
                break

            else: # different color piece (opponent)
                last = [current]
                
            left -= 1

        return moves


    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step): # what row we are starting and stopping by and by what step
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0: # empty square
                if skipped and not last:
                    break
                elif skipped: # double jumping ?
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
                 
            elif current.color == color: # if same color piece is there
                break

            else: # different color piece (opponent)
                last = [current]
                
            right += 1
        
        return moves