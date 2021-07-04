import pygame
from .constants import WHITE, ROWS, COLS, GREEN, SEA_GREEN, SQUARE_SIZE, NEUTRAL_PLAYER, SECOND_PLAYER, FIRST_PLAYER, RED
from .card import Card


class Board:
    def __init__(self, screen, total_enemy_card, board, player):
        self.board = []
        self.second_player_deck = dict()
        self.selected_piece = None
        self.black_left = self.white_left = 4
        self.board_bg = pygame.image.load('assets/board.png')
        self.board_bg = pygame.transform.scale(self.board_bg, (1400, 750))
        self.screen = screen
        self.create_board(board, player.cards)
        self.generate_second_player_cards(total_enemy_card)

    def generate_second_player_cards(self, total_enemy_card):
        for i in range(total_enemy_card):
            self.second_player_deck[(
                10+i, -1)] = Card(10 + i, -1, 0, 1, SECOND_PLAYER, False)

    def draw_squares(self):
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
        pivot_card_left = pivot_card_right = self.board[row][col]
        # left
        idx_left = idx_right = row
        while idx_left >= 0:
            is_card_direction_top = pivot_card_left.direction == "top"
            card = self.board[idx_left][col]
            nextCard = self.board[idx_left-1][col]
            if not isinstance(card, Card):
                index = idx_left
                if not is_card_direction_top:
                    index = idx_left
                left_row = index
                break
            else:
                pivot_card_left = self.board[idx_left][col]
                if card.direction == "top":
                    idx_left = idx_left - 1
                else:
                    idx_left = idx_left - 2

        # right
        while idx_right < ROWS:
            is_card_direction_top = pivot_card_right.direction == "top"
            card = self.board[idx_right][col]
            if not isinstance(card, Card):
                index = idx_right
                if not is_card_direction_top:
                    index = idx_right
                right_row = index
                break
            else:
                pivot_card_right = self.board[idx_right][col]
                if card.direction == "top":
                    idx_right = idx_right + 1
                else:
                    idx_right = idx_right + 2
        return left_row, right_row, col, pivot_card_left, pivot_card_right

    def draw_hint_tile(self, left_row, right_row, col):
        pygame.draw.rect(self.screen, RED, ((left_row * SQUARE_SIZE) + 100,
                                            (col * SQUARE_SIZE) + 75, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.screen, RED, ((right_row * SQUARE_SIZE) + 100,
                                            (col * SQUARE_SIZE) + 75, SQUARE_SIZE, SQUARE_SIZE))
        pygame.display.flip()

    def move(self, card, dest_row, dest_col):
        self.board[card.row][card.col], self.board[dest_row][dest_col] = 0, self.board[card.row][card.col]
        card.move(dest_row, dest_col)

    def get_card(self, row, col):
        if col >= 0 and col <= 18:
            card = self.board[row][col]
        else:
            card = None
        return card

    def create_board(self, board, first_player_cards):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                # initialize middle card
                if board[row][col] != 0:
                    current_card = board[row][col]
                    self.board[row].append(
                        Card(row, col, current_card[0], current_card[1], NEUTRAL_PLAYER, True))
                else:
                    self.board[row].append(0)
            # initialize first player card
            if row >= 10 and row <= 10 + 2:
                self.board[row].append(
                    Card(row, 18, first_player_cards[row - 10][0], first_player_cards[row - 10][1], FIRST_PLAYER, False))
            else:
                self.board[row].append(0)
        print(self.board)

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
