from typing import Tuple, Any
from pygame_menu.examples import create_example_window
import pygame_menu
from network import NetworkThread
from gui.card import Card
from gui.board import Board
import pygame
import sys
from pygame.locals import *
from gui.constants import HEIGHT, WIDTH, SQUARE_SIZE, WHITE, GREEN_CHAT, BLACK, GRAY, DARK_GRAY, MORE_DARK_GRAY, BROWN, RED
from gui.player import Player

pygame.init()
pygame.display.set_caption('Domino')
surface = pygame.display.set_mode((640, 360))
pygame.font.init()
menu_font = pygame.font.SysFont(pygame_menu.font.FONT_BEBAS, 50)
main_font = pygame.font.SysFont(pygame_menu.font.FONT_BEBAS, 40)
chat_font = pygame.font.SysFont(pygame_menu.font.FONT_BEBAS, 25)
username_font = pygame.font.SysFont(pygame_menu.font.FONT_BEBAS, 20)


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
        self.FPS = 60
        self.network = None
        self.player = None
        self.result = None
        self.messages = []
        self.input_name()

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
                    self.network.disconnect()
                    self.close_game()
            pygame.display.update()
        self.play_game()

    def display_main(self):
        if len(self.user_name.get_value()) > 0:
            self.menu.clear()
            self.menu.add.image(self.image, angle=0, scale=(0.15, 0.15))
            play_button = self.menu.add.button(
                'Play', self.start_the_game, button_id='Play')
            highscore_button = self.menu.add.button(
                'Highscore', self.get_highscore, button_id='Highscore')
            self.menu.add.button(
                'Quit', pygame_menu.events.EXIT, button_id="quit")

    def get_highscore(self):
        f = open("highscore.txt", "r")
        highscore = f.read()
        self.menu.clear()
        self.menu.add.label("High Score", max_char=70, font_size=40)
        self.menu.add.label(highscore, max_char=120, font_size=20)
        self.menu.add.button("Return", self.display_main, button_id="return 1")

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
                left_row, right_row, hint_col, pivot_card_left, pivot_card_right = self.board.get_hint_tile()
                msg = {
                    'status': 'time_out',
                    'card': None,
                    'pivot_card_left': pivot_card_left.serialize_data(),
                    'pivot_card_right': pivot_card_right.serialize_data(),
                }
                self.network.send_to_server(msg)

    def render_chat(self):
        if self.messages:
            for idx, data in enumerate(self.messages):
                player_id, chat, username = data
                message_text = chat_font.render(chat, True, BLACK)
                width, height = message_text.get_size()
                if player_id == self.player.id:
                    side = 200
                    chat_color = GREEN_CHAT
                    pos_x = 1535 - width - 40
                else:
                    side = 0
                    chat_color = WHITE
                    pos_x = 1125

                chat_box = pygame.Rect(
                    pos_x, 120 + 50 * idx, width + 30, height + 20)
                pygame.draw.rect(self.surface, chat_color, chat_box, 0, 5)

                if player_id != self.player.id:
                    username_text = username_font.render(
                        username, True, MORE_DARK_GRAY)
                    self.surface.blit(
                        username_text, (chat_box.x+5, chat_box.y-10))

                self.surface.blit(
                    message_text, (chat_box.x+15, chat_box.y+10))

    def render_winner(self):
        winner_id = self.result['winner']
        state = ''
        if self.result['my_value'] == self.result['enemy_value']:
            state = 'Draw'
            color = BROWN
        elif winner_id == self.player.id:
            state = 'Win'
            color = GREEN_CHAT
        else:
            state = 'Lose'
            color = RED

        my_username = self.user_name.get_value()
        my_value_state = 'Kartu sisa {}(Anda) bernilai: {}'.format(
            my_username, self.result['my_value'])
        my_value_text = main_font.render(my_value_state, True, WHITE)

        enemy_value_state = 'Kartu sisa {}(Lawan) bernilai: {}'.format(
            self.result['enemy_username'], self.result['enemy_value']
        )
        enemy_value_text = main_font.render(enemy_value_state, True, WHITE)

        width1 = enemy_value_text.get_size()[0]
        width2 = my_value_text.get_size()[0]
        width = width1 if width1 > width2 else width2

        result_text = main_font.render(state, True, WHITE)
        result_box = pygame.Rect(250, 100, width + 70, 200)

        pygame.draw.rect(self.surface, color, result_box, 0, 20)
        self.surface.blit(result_text, (result_box.x +
                          (width//2), result_box.y+25))
        self.surface.blit(my_value_text, (result_box.x+40, result_box.y+75))
        self.surface.blit(enemy_value_text,
                          (result_box.x+40, result_box.y+125))

    def play_game(self):
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        running = True
        self.board = self.init_game()
        is_card_drag = False
        is_showing_hint_tile = False

        input_box = pygame.Rect(1125, 640, 385, 50)
        inactive_color_input_box = WHITE
        active_color_input_box = BLACK
        color_input_box = inactive_color_input_box
        is_input_box_active = False

        button = pygame.Rect(1275, 700, 100, 50)
        is_button_active = False
        active_color_button = MORE_DARK_GRAY
        inactive_color_button = DARK_GRAY
        color_button = inactive_color_button
        self.text = ''

        main_menu_btn_text = chat_font.render("Main Menu", True, WHITE)
        btn_width = main_menu_btn_text.get_size()[0]
        btn_main_menu = pygame.Rect(900, 10, btn_width + 20, 40)

        msg = {
            'status': 'send_username',
            'username': self.user_name.get_value()
        }
        self.network.send_to_server(msg)
        while running:
            try:
                self.surface.fill(WHITE)
                clock.tick(self.FPS)
                self.board.draw()

                chat_bg = pygame.Rect(1122, 0, 420, 750)
                pygame.draw.rect(self.surface, GRAY, chat_bg)
                chat_title = main_font.render("CHAT", True, MORE_DARK_GRAY)
                self.surface.blit(chat_title, (chat_bg.x+180, chat_bg.y+70))

                position = pygame.mouse.get_pos()

                inactive_bg = pygame.Rect(1125, 640, 385, 50)
                pygame.draw.rect(self.surface, WHITE, inactive_bg)

                if is_input_box_active:
                    pygame.draw.rect(
                        self.surface, color_input_box, input_box, 2)
                else:
                    pygame.draw.rect(self.surface, color_input_box, input_box)

                txt_surface = chat_font.render(self.text, True, BLACK)
                self.surface.blit(txt_surface, (input_box.x+5, input_box.y+5))

                pygame.draw.rect(self.surface, color_button, button, 0, 10)
                btn_text = chat_font.render("Kirim", True, WHITE)
                self.surface.blit(btn_text, (button.x+30, button.y+17))

                if self.network.is_sending and not self.network.is_waiting:
                    if 'state' in self.network.data and self.network.data['state'] == 2:
                        player_data = self.network.data['player']
                        self.player = Player(
                            player_data['id'], player_data['cards'], player_data['status'])
                        board_data = self.network.data['board']
                        self.board = Board(
                            self.surface, board_data['total_enemy_card'], board_data['board'], self.player, board_data['current_turn'])
                        self.board.current_turn = board_data['current_turn']
                    elif 'state' in self.network.data and self.network.data['state'] == 3:
                        self.messages = self.network.data['messages']
                    elif 'state' in self.network.data and self.network.data['state'] == 4:
                        player_data = self.network.data['player']
                        self.player = Player(
                            player_data['id'], player_data['cards'], player_data['status'])
                        board_data = self.network.data['board']
                        self.board = Board(
                            self.surface, board_data['total_enemy_card'], board_data['board'], self.player, board_data['current_turn'])
                        self.board.current_turn = 'none'
                        self.result = self.network.data
                    self.network.is_sending = False

                self.render_time()

                self.render_chat()

                if self.result:
                    self.render_winner()
                    # render main menu
                    pygame.draw.rect(self.surface, MORE_DARK_GRAY,
                                     btn_main_menu, 0, 10)
                    self.surface.blit(
                        main_menu_btn_text, (btn_main_menu.x+10, btn_main_menu.y+10))

                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        running = False
                        self.network.disconnect()
                        self.close_game()
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if not is_card_drag and self.board.current_turn == self.player.status:
                            last_row, last_col = self.get_row_and_column_from_mouse(
                                position)
                            if self.board.is_in_board_limit(last_row, last_col):
                                card = self.board.get_card(last_row, last_col)
                                if isinstance(card, Card) and not card.is_in_board:
                                    is_showing_hint_tile = True
                                    left_row, right_row, hint_col, pivot_card_left, pivot_card_right = self.board.get_hint_tile()
                                    if not self.board.is_two_card_has_same_value(pivot_card_left, card):
                                        left_row = -1
                                    if not self.board.is_two_card_has_same_value(pivot_card_right, card):
                                        right_row = -1
                                    is_card_drag = True

                        # handle chat
                        if input_box.collidepoint(ev.pos):
                            # Toggle the active variable.
                            is_input_box_active = not is_input_box_active
                        else:
                            is_input_box_active = False

                        if button.collidepoint(ev.pos) and len(self.text) > 0:
                            #
                            msg = {
                                'status': 'send_msg',
                                'chat': self.text,
                                'username': self.user_name.get_value()
                            }
                            self.network.send_to_server(msg)
                            self.text = ''
                            # Toggle the active variable.
                            is_button_active = not is_button_active
                        else:
                            is_button_active = False

                        if btn_main_menu.collidepoint(ev.pos):
                            running = False
                        color_input_box = active_color_input_box if is_input_box_active else inactive_color_input_box
                        color_button = active_color_button if is_button_active else inactive_color_button
                    if ev.type == pygame.KEYDOWN:
                        if is_input_box_active:
                            if ev.key == pygame.K_RETURN and len(self.text) > 0:
                                msg = {
                                    'status': 'send_msg',
                                    'chat': self.text,
                                    'username': self.user_name.get_value()
                                }
                                self.network.send_to_server(msg)
                                self.text = ''
                                # Toggle the active variable.
                                is_button_active = not is_button_active
                            elif ev.key == pygame.K_BACKSPACE:
                                self.text = self.text[:-1]
                            else:
                                text_width = txt_surface.get_size()[0]
                                if ev.key >= 32 and ev.key <= 126:
                                    if pygame.KMOD_SHIFT:
                                        ev.key -= 32
                                    if text_width < 337:
                                        self.text += ev.unicode

                    if ev.type == pygame.MOUSEBUTTONUP and is_card_drag:
                        is_card_drag = False
                        is_showing_hint_tile = False
                        dest_row, dest_col = self.get_row_and_column_from_mouse(
                            position)
                        if isinstance(card, Card) and not card.is_in_board \
                                and self.board.is_in_board_limit(dest_row, dest_col) and not card.is_in_last_col():
                            if (left_row == card.row and card.col == hint_col) or (right_row == card.row and card.col == hint_col):
                                card.update_status_in_board()
                                if left_row == card.row:
                                    position = "left"
                                    pivot_card = pivot_card_left
                                else:
                                    position = "right"
                                    pivot_card = pivot_card_right

                                card.rotate_card(
                                    self.surface, pivot_card, position)
                                msg = {
                                    'status': 'send_card',
                                    'card': card.serialize_data(),
                                    'pivot_card_left': pivot_card_left.serialize_data(),
                                    'pivot_card_right': pivot_card_right.serialize_data(),
                                }
                                self.network.send_to_server(msg)
                            else:
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
            except KeyboardInterrupt:
                running = False
        # disconnect
        print("sini")
        self.network.disconnect()
        self.restart_display()

    def restart_display(self):
        self.surface = pygame.display.set_mode((640, 360))
        self.theme = self.init_theme()
        self.image = "assets/logo.png"
        self.wait = "Waiting for other player to join"
        self.menu = pygame_menu.Menu(
            height=360,
            theme=self.theme,
            title='Main Menu',
            width=640
        )
        self.menu.add.image(self.image, angle=0, scale=(0.15, 0.15))
        self.FPS = 60
        self.network = None
        self.player = None
        self.result = None
        self.messages = []
        self.display_main()
        self.menu.mainloop(self.surface)

    def close_game(self):
        pygame_menu.events.EXIT
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    game = Game(surface)
    game.menu.mainloop(game.surface)
