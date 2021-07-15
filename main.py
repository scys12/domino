from typing import Tuple, Any
from pygame_menu.examples import create_example_window
import pygame_menu
from network import NetworkThread
from gui.card import Card
from gui.board import Board
import pygame
import sys
from pygame.locals import *
from gui.constants import HEIGHT, WIDTH, SQUARE_SIZE, WHITE
from gui.player import Player

pygame.init()
pygame.display.set_caption('Domino')
surface = pygame.display.set_mode((640, 360))
pygame.font.init()
menu_font = pygame.font.SysFont(pygame_menu.font.FONT_BEBAS, 50)
main_font = pygame.font.SysFont(pygame_menu.font.FONT_BEBAS, 40)


class Game:
    def __init__(self, surface):
        self.surface = surface
        self.theme = self.init_theme()
        self.user_name = None
        self.image = "assets/logo.png"
        self.wait = "Waiting for other player to join"
        self.menu = pygame_menu.Menu(
            height=360,
            theme=self.theme,
            title='Main Menu',
            width=640
        )
        self.menu.add.image(self.image, angle=0, scale=(0.15, 0.15))
        self.input_name()
        self.FPS = 60
        self.network = None
        self.player = None

    def init_theme(self):
        mytheme = pygame_menu.themes.THEME_GREEN.copy()
        mytheme.title_font = pygame_menu.font.FONT_FRANCHISE
        mytheme.widget_font = pygame_menu.font.FONT_BEBAS
        return mytheme

    def input_name(self):
        self.menu.add.label(title="Masukkan    Nama")
        self.user_name = self.menu.add.text_input(
            'Name: ', default='', maxchar=10)
        self.menu.add.button('Enter', self.display_main, button_id='quit')

    def start_the_game(self):
        print('{0}, Do the job here!'.format(self.user_name.get_value()))
        self.network = NetworkThread()
        self.network.start()
        clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((640, 360))
        while self.network.is_waiting:
            self.menu.add.label(self.wait, max_char=40, font_size=20)
            clock.tick(self.FPS)
            self.surface.fill((186, 214, 177))
            textsurface = menu_font.render(
                'Waiting for other player to join...', True, WHITE)
            self.surface.blit(textsurface, (640//2-250, 360//2))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                    self.close_game()
            pygame.display.update()
        self.play_game()

    def display_main(self):
        if len(self.user_name.get_value()) > 0:
            self.menu.clear()
            self.menu.add.image(self.image, angle=0, scale=(0.15, 0.15))
            play_button = self.menu.add.button(
                'Play', self.start_the_game, button_id='Play')
            self.menu.add.button(
                'Quit', pygame_menu.events.EXIT, button_id="quit")

    def get_row_and_column_from_mouse(self, position):
        x, y = position
        row = (x - 100) // SQUARE_SIZE
        col = (y - 75) // SQUARE_SIZE
        return row, col

    def init_game(self):
        if 'state' in self.network.data and self.network.data['state'] == 1:
            player_data = self.network.data['player']
            self.player = Player(
                player_data['id'], player_data['cards'], player_data['status'])
            board_data = self.network.data['board']
            return Board(self.surface, board_data['total_enemy_card'], board_data['board'], self.player, board_data['current_turn'])

    def render_time(self):
        if self.board.current_turn == self.player.status and not self.network.is_waiting:
            if not self.player.is_time_out():
                self.player.update_time()
                image = pygame.image.load('assets/timer.png')
                image = pygame.transform.smoothscale(
                    image.convert_alpha(), (50, 50))
                if self.player.timer == 60:
                    time_render = '01:00'
                else:
                    time_render = '00:' + str(self.player.timer).zfill(2)
                textsurface = main_font.render(time_render, True, WHITE)
                pygame.draw.rect(self.surface, WHITE,
                                 pygame.Rect(1, 2, 130, 65),  3)
                self.surface.blit(image, (0, 10))
                self.surface.blit(textsurface, (50, 20))
            else:
                print("ok")
                self.network.send_card('time_out', None)

    def play_game(self):
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        running = True
        self.board = self.init_game()
        is_card_drag = False
        is_showing_hint_tile = False
        while running:
            self.surface.fill(WHITE)
            clock.tick(self.FPS)
            if self.network.is_sending and not self.network.is_waiting:
                player_data = self.network.data['player']
                self.player = Player(
                    player_data['id'], player_data['cards'], player_data['status'])
                board_data = self.network.data['board']
                self.board = Board(
                    self.surface, board_data['total_enemy_card'], board_data['board'], self.player, board_data['current_turn'])
                self.board.current_turn = board_data['current_turn']
                self.network.is_sending = False

            self.board.draw()

            self.render_time()

            position = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                    self.close_game()
                if ev.type == pygame.MOUSEBUTTONDOWN and not is_card_drag and self.board.current_turn == self.player.status:
                    last_row, last_col = self.get_row_and_column_from_mouse(
                        position)
                    card = self.board.get_card(last_row, last_col)
                    if isinstance(card, Card) and not card.is_in_board:
                        is_showing_hint_tile = True
                        left_row, right_row, hint_col, pivot_card_left, pivot_card_right = self.board.get_hint_tile()
                        if not self.board.is_two_card_has_same_value(pivot_card_left, card):
                            left_row = -1
                        if not self.board.is_two_card_has_same_value(pivot_card_right, card):
                            right_row = -1
                        print(left_row, right_row, hint_col)
                        is_card_drag = True
                if ev.type == pygame.MOUSEBUTTONUP and is_card_drag:
                    is_card_drag = False
                    is_showing_hint_tile = False
                    dest_row, dest_col = self.get_row_and_column_from_mouse(
                        position)
                    if isinstance(card, Card) and not card.is_in_board \
                            and self.board.is_in_board_limit(dest_row, dest_col) and not card.is_in_last_col():
                        print("JADI")
                        if (left_row == dest_row and dest_col == hint_col) or (right_row == dest_row and dest_col == hint_col):
                            card.update_status_in_board()
                            print("LEFT")
                            print(left_row, dest_row)
                            print("COL")
                            print(dest_col, hint_col)
                            print("RIGHT")
                            print(right_row, dest_row)
                            if left_row == dest_row:
                                position = "left"
                                pivot_card = pivot_card_left
                            else:
                                position = "right"
                                pivot_card = pivot_card_right

                            card.rotate_card(
                                self.surface, pivot_card, dest_row, dest_col, position)

                            self.network.send_card(
                                'send_card', card.serialize_data())
                        else:
                            print("GK JADI")
                            self.board.move(card, last_row, last_col)
                if ev.type == pygame.MOUSEMOTION and is_card_drag:
                    row, col = self.get_row_and_column_from_mouse(position)
                    existing_card = self.board.get_card(row, col)
                    if isinstance(card, Card) and not existing_card and self.board.is_in_board_limit(row, col):
                        self.board.move(card, row, col)
            if is_showing_hint_tile:
                if left_row != -1:
                    self.board.draw_hint_tile(left_row, hint_col)
                if right_row != -1:
                    self.board.draw_hint_tile(right_row, hint_col)
            pygame.display.update()

    def close_game(self):
        pygame_menu.events.EXIT
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    game = Game(surface)
    game.menu.mainloop(game.surface)
