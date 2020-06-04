import pygame
from pygame.locals import *
import sys
import os


def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


os.environ['SDL_VIDEO_WINDOW_POS'] = '1'

pygame.init()
win_size = [pygame.display.Info().current_w - 5, pygame.display.Info().current_h - 40]
DS = pygame.display.set_mode(size=win_size)
CLOCK = pygame.time.Clock()
FPS = 120

x = 0

# main loop
while True:
    events()

    startColor = (0, 0, 0)
    endColor = (255, 255, 255)

    for y in range(win_size[1]):
        r = y, 0, win_size[1] - 1, startColor[0], endColor[0]
        g = y, 0, win_size[1] - 1, startColor[1], endColor[1]
        b = y, 0, win_size[1] - 1, startColor[2], endColor[2]
        pygame.draw.line(DS, (round(r), round(g), round(b)), (0, y), (win_size[0] - 1, y))

    DS.blit(pygame.transform.scale(DS, win_size), (0, 0))
    pygame.display.update()
    CLOCK.tick(FPS)
