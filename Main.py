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
screen = pg.display.set_mode((info_object.current_w - 5, info_object.current_h - 40))
pg.display.set_caption('Rocket Wave')


# Loop principal
def game_loop():
    game_exit = False
    while not game_exit:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game_exit = True


game_loop()
pg.quit()
exit()
