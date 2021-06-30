import pygame
from constants import WHITE, ROWS, COLS, GREEN, SEA_GREEN, SQUARE_SIZE, NEUTRAL_PLAYER, SECOND_PLAYER, FIRST_PLAYER, RED
from .card import Card


class Board:
    def __init__(self, screen):
        self.board = []
        self.second_player_deck = dict()
        self.selected_piece = None
        self.black_left = self.white_left = 4
        self.board_bg = pygame.image.load('assets/board.png')
        self.board_bg = pygame.transform.scale(self.board_bg, (1400, 750))
        self.screen = screen
        self.create_board()
        self.generate_second_player_cards()

    def generate_second_player_cards(self):
        for i in range(2):
            self.second_player_deck[(
                10+i, -1)] = Card(10 + i, -1, 0, 1, SECOND_PLAYER, False)

    def draw_squares(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.board_bg, (0, 0))
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.screen, SEA_GREEN, ((row * SQUARE_SIZE) + 100,
                                 (col * SQUARE_SIZE) + 75, SQUARE_SIZE, SQUARE_SIZE))
            for col in range(row % 2 != 1, COLS, 2):
                pygame.draw.rect(self.screen, GREEN, ((row * SQUARE_SIZE) + 100,
                                 (col * SQUARE_SIZE) + 75, SQUARE_SIZE, SQUARE_SIZE))

    def is_in_board_limit(self, row, col):
        return row >= 0 and row < 28 and col >= 0 and col <= 18

    def get_hint_tile(self):
        row = ROWS//2-1
        col = COLS//2-1
        for idx in range(row, -1, -1):
            card = self.board[idx][col]
            if not isinstance(card, Card):
                left_row = idx
                break
        for idx in range(row, ROWS):
            card = self.board[idx][col]
            if not isinstance(card, Card):
                right_row = idx
                break
        return left_row, right_row, col

    def draw_hint_tile(self, left_row, right_row, col):
        pygame.draw.rect(self.screen, RED, ((left_row * SQUARE_SIZE) + 100,
                                            (col * SQUARE_SIZE) + 75, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.screen, RED, ((right_row * SQUARE_SIZE) + 100,
                                            (col * SQUARE_SIZE) + 75, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, card, dest_row, dest_col):
        self.board[card.row][card.col], self.board[dest_row][dest_col] = 0, self.board[card.row][card.col]
        card.move(dest_row, dest_col)

    def get_card(self, row, col):
        if col >= 0 and col <= 18:
            card = self.board[row][col]
        else:
            card = None
        return card

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == ROWS//2-1 and col == COLS//2-1:
                    self.board[row].append(
                        Card(row, col, 0, 1, NEUTRAL_PLAYER, True))
                else:
                    self.board[row].append(0)
            if row >= 10 and row <= 10 + 2:
                self.board[row].append(
                    Card(row, 18, 0, 2, NEUTRAL_PLAYER, False))
            else:
                self.board[row].append(0)

    def draw(self):
        self.draw_squares()
        for row in range(ROWS):
            for col in range(COLS+1):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(self.screen)

        for row, col in self.second_player_deck.keys():
            piece = self.second_player_deck[(row, col)]
            if piece != 0:
                piece.draw(self.screen)
