import pygame
import os


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('"Trocar nome"')
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()
