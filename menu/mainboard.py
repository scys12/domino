import sys
sys.path.append('..')
from gui.constants import HEIGHT, WIDTH, SQUARE_SIZE
from gui.board import Board
from gui.card import Card

class MainBoard:
    def __init__(self, network, pygame) -> None:
        self.network = network
        self.FPS = 60
        self.pygame = pygame

    def get_row_and_column_from_mouse(position):
        x, y = position
        row = (x - 100) // SQUARE_SIZE
        col = (y - 75) // SQUARE_SIZE
        return row, col


    def start_game(self):
        screen = self.pygame.display.set_mode((WIDTH, HEIGHT))
        clock = self.pygame.time.Clock()
        running = True
        board = Board(screen)
        is_card_drag = False
        is_showing_hint_tile = False
        # network = NetworkThread()
        # network.start()
        while running:
            clock.tick(self.FPS)
            board.draw()
            for ev in self.pygame.event.get():
                if ev.type == self.pygame.QUIT:
                    running = False
                if ev.type == self.pygame.MOUSEBUTTONDOWN and not is_card_drag:
                    position = self.pygame.mouse.get_pos()
                    last_row, last_col = self.get_row_and_column_from_mouse(position)
                    card = board.get_card(last_row, last_col)
                    if isinstance(card, Card) and not card.is_in_board:
                        is_showing_hint_tile = True
                        left_row, right_row, hint_col = board.get_hint_tile()
                        is_card_drag = True
                if ev.type == self.pygame.MOUSEBUTTONUP:
                    is_card_drag = False
                    is_showing_hint_tile = False
                    position = self.pygame.mouse.get_pos()
                    row, col = self.get_row_and_column_from_mouse(position)
                    if isinstance(card, Card) and not card.is_in_board \
                            and board.is_in_board_limit(row, col) and not card.is_in_last_col():
                        if (left_row == row and col == hint_col) or (right_row == row and col == hint_col):
                            card.update_status_in_board()
                            if left_row == row:
                                pivot_card = board.get_card(left_row+1, hint_col)
                            else:
                                pivot_card = board.get_card(right_row-1, hint_col)
                            card.rotate_card(screen, pivot_card, row, col)
                        else:
                            board.move(card, last_row, last_col)
                if ev.type == self.pygame.MOUSEMOTION and is_card_drag:
                    position = self.pygame.mouse.get_pos()
                    row, col = self.get_row_and_column_from_mouse(position)
                    existing_card = board.get_card(row, col)
                    if isinstance(card, Card) and not existing_card and board.is_in_board_limit(row, col):
                        board.move(card, row, col)
            if is_showing_hint_tile:
                board.draw_hint_tile(left_row, right_row, hint_col)
            self.pygame.display.update()
        self.pygame.quit()
