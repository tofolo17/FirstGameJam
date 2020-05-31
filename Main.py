import pygame as pg
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Verificando erros de inicializacao
check_errors = pg.init()
if check_errors[1] > 0:
    print(f"(!) Ops, {check_errors[1]} o Pygame iniciou com algum problema...")
    sys.exit(-1)
else:
    print("(+) O Pygame foi inicializado com sucesso!")

# Tamanho da tela e título
info_object = pg.display.Info()
w = info_object.current_w - 5
h = info_object.current_h - 40
screen = pg.display.set_mode((w, h))
pg.display.set_caption('Rocket Wave')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)


def game_intro():
    x = 0
    intro = True
    bg = pg.image.load('Imagens//background.jpg').convert()
    while intro:
        rel_x = x % bg.get_rect().width
        screen.blit(bg, (rel_x - bg.get_rect().width, 0))
        if rel_x < w:
            screen.blit(bg, (rel_x, 0))
        x -= 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    intro = False
        pg.display.update()


# Loop principal
def game_loop():
    game_exit = False
    while not game_exit:
        screen.fill(black)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game_exit = True
        pg.display.update()


game_intro()
game_loop()
pg.quit()
exit()
