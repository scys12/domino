from menu.mainboard import MainBoard
import pygame_menu
from pygame_menu.examples import create_example_window
from typing import Tuple, Any
from network import NetworkThread

class Menu:
    def __init__(self, screen, pygame):
        self.surface = screen
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
        self.pygame = pygame
        self.mainboard = None

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
        network = NetworkThread()
        network.start()

        print(network.status)
        if(network.status == "Anda sudah terpasangkan"):
            pygame_menu.events.EXIT
            self.mainboard = MainBoard(network, self.pygame)
            self.mainboard.start_game()

        print('{0}, Do the job here!'.format(self.user_name.get_value()))
        self.menu.remove_widget("Play")
        self.menu.remove_widget("quit")
        self.menu.add.button("Return", self.display_main, button_id='Return')
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.add.label(self.wait, max_char=40, font_size=20)

    def display_main(self):
        if len(self.user_name.get_value()) > 0:
            self.menu.clear()
            self.menu.add.image(self.image, angle=0, scale=(0.15, 0.15))
            play_button = self.menu.add.button(
                'Play', self.start_the_game, button_id='Play')
            self.menu.add.button(
                'Quit', pygame_menu.events.EXIT, button_id="quit")
