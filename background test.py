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

bkgd = pygame.image.load("Imagens//test.png").convert()
x = 0

# main loop
while True:
    events()

    rel_x = x % bkgd.get_rect().width
    DS.blit(bkgd, (rel_x - bkgd.get_rect().width, 0))
    if rel_x < win_size[0]:
        DS.blit(bkgd, (rel_x, 0))
    x -= 1

    DS.blit(pygame.transform.scale(DS, win_size), (0, 0))
    pygame.display.update()
    CLOCK.tick(FPS)
