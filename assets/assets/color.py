import pygame as pg
import random

if __name__ == '__main__':
    running = True
    pg.init()
    screen = pg.display.set_mode((600, 400))
    screen_rect = screen.get_rect()
    clock = pg.time.Clock()
    timer = 0
    bg = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    while running:
        screen.fill(bg)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if pg.time.get_ticks() - timer > 100:
            timer = pg.time.get_ticks()
            bg = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pg.display.update()
        clock.tick(10)