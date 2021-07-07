import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Tuple, Any
surface = create_example_window('Simple Domino', (640, 360))
mytheme = pygame_menu.themes.THEME_GREEN.copy()
mytheme.title_font = pygame_menu.font.FONT_FRANCHISE
mytheme.widget_font = pygame_menu.font.FONT_BEBAS

user_name = None

menu = pygame_menu.Menu(
    height=360,
    theme=mytheme,
    title='Main Menu',
    width=640
)

wait = "Waiting for other player to join"

f = open("highscore.txt", "r")
highscore = f.read()
print(highscore)

def highscore_menu():
    menu.remove_widget("Play")
    menu.remove_widget("quit")
    menu.remove_widget("highscore")
    menu.add.label("High Score", max_char=70, font_size=40)
    menu.add.label(highscore, max_char=120, font_size=20)
    menu.add.button("Return", refresh, button_id="return 1")

def transition():
    menu.clear()
    menu.add.image(image, angle=0, scale=(0.15, 0.15))
    refresh()

def input_name():
    global user_name
    menu.add.label(title="Masukkan     Nama")
    user_name = menu.add.text_input('Name: ', default='', maxchar=10)
    menu.add.button('Enter', display_main, button_id='quit')


def start_the_game():
    print('{0}, Do the job here!'.format(user_name.get_value()))
    menu.remove_widget("Play")
    menu.remove_widget("quit")
    menu.remove_widget("highscore")
    menu.add.button("Return", display_main, button_id='Return')
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.add.label(wait, max_char=40, font_size=20)

def refresh():
    menu.clear()
    image = "./logo.png"
    welcome = 'Welcome, {0}!'.format(user_name.get_value())
    menu.add.image(image, angle=0, scale=(0.15, 0.15))
    menu.add.label(welcome, max_char=40, font_size=20)
    play_button = menu.add.button('Play', start_the_game, button_id='Play')
    menu.add.button("Highscore", highscore_menu, button_id="highscore")
    menu.add.button('Quit', pygame_menu.events.EXIT, button_id="quit")


def display_main():
    global user_name
    if len(user_name.get_value()) > 0:
        menu.clear()
        image = "./logo.png"
        welcome = 'Welcome, {0}!'.format(user_name.get_value())
        menu.add.image(image, angle=0, scale=(0.15, 0.15))
        menu.add.label(welcome, max_char=40, font_size=20)
        play_button = menu.add.button('Play', start_the_game, button_id='Play')
        menu.add.button("Highscore", highscore_menu, button_id="highscore")
        menu.add.button('Quit', pygame_menu.events.EXIT, button_id="quit")


image = "./logo.png"
menu.add.image(image, angle=0, scale=(0.15, 0.15))
input_name()

if __name__ == '__main__':
    menu.mainloop(surface)
