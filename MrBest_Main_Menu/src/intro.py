import pygame
import chess_game

pygame.init()

class Intro():
    size = (700, 500)

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()