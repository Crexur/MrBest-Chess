import pygame, sys

def load_gif(filename):
    gif = pygame.image.load(filename)
    gif.set_colorkey((255,255,255), pygame.RLEACCEL)
    return gif

pygame.init()

screen = pygame.display.set_mode((600, 600))

gif_surface = load_gif("giphy.gif")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(gif_surface, (0, 0))
    pygame.display.update()

#Wala lang toh