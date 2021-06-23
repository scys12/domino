import pygame
from pygame.locals import *
from constants import HEIGHT, WIDTH
from model.board import Board

FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Domino')


def main():
    clock = pygame.time.Clock()
    running = True
    board = Board()

    while running:
        clock.tick(FPS)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
        board.draw_squares(screen)
        pygame.display.update()
    pygame.quit()


main()
