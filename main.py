import pygame
from pygame.locals import *
from constants import HEIGHT, WIDTH, SQUARE_SIZE
from model.board import Board
from model.card import Card

FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Domino')


def get_row_and_column_from_mouse(position):
    x, y = position
    row = (x - 100) // SQUARE_SIZE
    col = (y - 75) // SQUARE_SIZE
    return row, col


def main():
    clock = pygame.time.Clock()
    running = True
    board = Board(screen)
    is_card_drag = False

    while running:
        clock.tick(FPS)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.MOUSEBUTTONDOWN:
                is_card_drag = True
                position = pygame.mouse.get_pos()
                last_row, last_col = get_row_and_column_from_mouse(position)
                card = board.get_card(last_row, last_col)
            if ev.type == pygame.MOUSEBUTTONUP:
                is_card_drag = False
                position = pygame.mouse.get_pos()
                row, col = get_row_and_column_from_mouse(position)
                if isinstance(card, Card) and not card.is_in_board and board.is_in_board_limit(row, col):
                    card.update_status_in_board()
            if ev.type == pygame.MOUSEMOTION and is_card_drag:
                position = pygame.mouse.get_pos()
                row, col = get_row_and_column_from_mouse(position)
                if isinstance(card, Card):
                    board.move(card, row, col)
        board.draw()
        pygame.display.update()
    pygame.quit()


main()
