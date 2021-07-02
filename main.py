import pygame
from pygame.locals import *
from menu.mainmenu import Menu

FPS = 60

pygame.init()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption('Domino')
main_menu = Menu(screen, pygame)

if __name__ == "__main__":
    main_menu.menu.mainloop(main_menu.surface)
