import pygame
from constants import SQUARE_SIZE, FIRST_PLAYER, NEUTRAL_PLAYER


class Card:
    def __init__(self, row, col, top, down, player, is_in_board):
        self.row = row
        self.col = col
        self.top = top
        self.down = down
        self.is_in_board = is_in_board
        self.player = player
        self.direction = 1
        self.x = 0
        self.y = 0
        self.calc_pos()

    def update_status_in_board(self):
        self.is_in_board = not self.is_in_board

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.row + 100
        self.y = SQUARE_SIZE * self.col + 75

    def draw(self, screen):
        if self.player != FIRST_PLAYER and self.player != NEUTRAL_PLAYER:
            image = pygame.image.load('assets/opponent.png')
            image = pygame.transform.scale(image, (30, 10))
        else:
            image = pygame.image.load('assets/01.png')
            image = pygame.transform.scale(image, (30, 40))
        screen.blit(image, (self.x, self.y))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
