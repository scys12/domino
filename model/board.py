import pygame
from constants import WHITE, ROWS, COLS, GREEN, SEA_GREEN, SQUARE_SIZE


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.black_left = self.white_left = 4

    def draw_squares(self, win):
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, SEA_GREEN, (row * SQUARE_SIZE,
                                 col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            for col in range(row % 2 != 1, COLS, 2):
                pygame.draw.rect(win, GREEN, (row * SQUARE_SIZE,
                                 col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        pass
