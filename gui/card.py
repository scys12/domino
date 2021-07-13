import pygame
from .constants import SQUARE_SIZE, FIRST_PLAYER, NEUTRAL_PLAYER


class Card:
    def __init__(self, row, col, top, down, player, is_in_board):
        self.row = row
        self.col = col
        self.top = top  # top always smaller than bottom
        self.down = down
        self.is_in_board = is_in_board
        self.player = player
        self.direction = "top"
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.position = "middle"
        self.image = None

    def rotate_card(self, screen, pivot_card, row, col, position):
        self.position = position
        if pivot_card.player == NEUTRAL_PLAYER:
            if position == "right":
                if self.top == pivot_card.top or self.top == pivot_card.down:
                    self.direction = "left"
                elif self.down == pivot_card.down or self.down == pivot_card.top:
                    self.direction = "right"
            elif position == "left":
                if self.top == pivot_card.top or self.top == pivot_card.down:
                    self.direction = "right"
                elif self.down == pivot_card.down or self.down == pivot_card.top:
                    self.direction = "left"
        else:
            if pivot_card.direction == "left":
                if pivot_card.down == self.top:
                    self.direction = "left"
                elif pivot_card.down == self.down:
                    self.direction = "right"
            if pivot_card.direction == "right":
                if pivot_card.down == self.top:
                    self.direction = "right"
                elif pivot_card.down == self.down:
                    self.direction = "left"

    def update_status_in_board(self):
        self.is_in_board = not self.is_in_board

    def is_in_last_col(self):
        return self.col == 18

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.row + 100
        self.y = SQUARE_SIZE * self.col + 75

    def draw(self, screen):
        self.image = self.get_image()
        if self.player == NEUTRAL_PLAYER:
            screen.blit(self.image, (self.x, self.y-15))
        else:
            if self.position == "middle" or self.position == "right":
                screen.blit(self.image, (self.x, self.y))
            elif self.position == "left":
                screen.blit(self.image, (self.x-34, self.y))

    def get_image(self):
        if self.player != FIRST_PLAYER and self.player != NEUTRAL_PLAYER:
            image = pygame.image.load('assets/opponent.png')
            image = pygame.transform.smoothscale(
                image.convert_alpha(), (30, 10))
        else:
            image = pygame.image.load(
                'assets/' + str(self.top) + str(self.down) + '.png')
            image = pygame.transform.smoothscale(
                image.convert_alpha(), (33, 67))
            if self.direction == "left":
                image = pygame.transform.rotate(image, 90)
            if self.direction == "right":
                image = pygame.transform.rotate(image, -90)
        return image

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def serialize_data(self):
        return {
            'row': self.row,
            'col': self.col,
            'top': self.top,
            'down': self.down,
            'is_in_board': self.is_in_board,
            'player': self.player,
            'direction': self.direction,
            'x': self.x,
            'y': self.y,
            'position': self.position,
            'image': self.image
        }
