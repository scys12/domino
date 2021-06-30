import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Tuple, Any
surface = create_example_window('Simple Domino', (640, 360))
mytheme = pygame_menu.themes.THEME_GREEN.copy()
mytheme.title_font=pygame_menu.font.FONT_FRANCHISE
mytheme.widget_font=pygame_menu.font.FONT_BEBAS

def start_the_game():
    global user_name
    print('{0}, Do the job here!'.format(user_name.get_value()))
    menu.remove_widget("Play")
    menu.remove_widget("quit")
    menu.add.button("Return", Refresh, button_id='Return')
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.add.label(wait, max_char=40, font_size=20)

def Refresh():
    menu.clear()
    image= "./logo.png"
    menu.add.image(image, angle=0, scale=(0.15, 0.15))
    user_name = menu.add.text_input('Name: ', default='Player 1', maxchar=10)
    play_button = menu.add.button('Play', start_the_game,button_id='Play')
    menu.add.button('Quit', pygame_menu.events.EXIT, button_id="quit")

menu = pygame_menu.Menu(
    height=360,
    theme=mytheme,
    title='Main Menu',
    width=640
)

wait = "Waiting for other player to join"

image= "./logo.png"
menu.add.image(image, angle=0, scale=(0.15, 0.15))
user_name = menu.add.text_input('Name: ', default='Player 1', maxchar=10)
play_button = menu.add.button('Play',start_the_game,button_id='Play')
menu.add.button('Quit', pygame_menu.events.EXIT, button_id='quit')

if __name__ == '__main__':
    menu.mainloop(surface)
