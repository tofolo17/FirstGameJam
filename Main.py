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
win_size = [info_object.current_w - 5, info_object.current_h - 40]
screen = pg.display.set_mode((win_size[0], win_size[1]))
pg.display.set_caption('Rocket Wave')
clock = pg.time.Clock()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

'''
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
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    intro = False
        pg.display.update()
        clock.tick(60)
'''


# Loop principal
def game_loop():

    # Variáveis do loop
    game_exit = False
    moving_right = False
    moving_left = False
    player_location = [50, 50]
    player_y_momentum = 0
    player_image = pg.image.load('Imagens//background.jpg').convert()
    player_rect = pg.Rect(player_location[0], player_location[1], player_image.get_width(), player_image.get_height())
    test_rect = pg.Rect(100, 100, 100, 50)

    # Enquanto o jogo estiver aberto...
    while not game_exit:

        # Atualizando a tela
        screen.fill(black)
        screen.blit(player_image, player_location)

        # Gravidade
        if player_location[1] > win_size[1] - player_image.get_height():
            player_y_momentum = -player_y_momentum
        else:
            player_y_momentum += 0.2
        player_location[1] += player_y_momentum

        # Velocidade
        if moving_right:
            player_location[0] += 4
        if moving_left:
            player_location[0] -= 4

        # Posições do rect do personagem
        player_rect.x = player_location[0]
        player_rect.y = player_location[1]

        # Teste de colisão
        if player_rect.colliderect(test_rect):
            pg.draw.rect(screen, (255, 0, 0), test_rect)
        else:
            pg.draw.rect(screen, (0, 255, 0), test_rect)

        # Apurando eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    moving_left = True
                if event.key == pg.K_RIGHT:
                    moving_right = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    moving_left = False
                if event.key == pg.K_RIGHT:
                    moving_right = False

        # Mostrando para o usuário e FPS
        pg.display.update()
        clock.tick(60)


# game_intro()
game_loop()
pg.quit()
sys.exit()
