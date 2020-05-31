import os
import sys

import pygame as pg

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()

# Tamanho da tela e título
win_size = [pg.display.Info().current_w - 5, pg.display.Info().current_h - 40]
screen = pg.display.set_mode(size=win_size)
pg.display.set_caption('Rocket Wave')
display = pg.Surface((300, 200))
clock = pg.time.Clock()

# Mapa
game_map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '2', '2', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2'],
            ['1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]
grass_img = pg.image.load('Imagens//grass.png')
dirt_img = pg.image.load('Imagens//dirt.png')

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


# Teste de colisão
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


# Detectando movimentos e colisões
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        if movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


# Loop principal
def game_loop():

    # Variáveis do loop
    game_exit = moving_left = moving_right = False

    # Variáveis físicas
    vertical_momentum = air_timer = timer = dt = 0

    # Personagem
    player_image = pg.image.load('Imagens//player.png').convert()
    player_image.set_colorkey((255, 255, 255))
    player_rect = pg.Rect(100, 116, 5, 13)

    # Enquanto o jogo estiver aberto...
    while not game_exit:

        # Atualizando a tela
        display.fill((146, 244, 255))

        # Construção do mapa
        tile_rect = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirt_img, (x * 16, y * 16))
                if tile == '2':
                    display.blit(grass_img, (x * 16, y * 16))
                if tile != '0':
                    tile_rect.append(pg.Rect(x * 16, y * 16, 16, 16))
                x += 1
            y += 1

        # Movimento do personagem
        player_movement = [0, 0]
        if moving_right:
            player_movement[0] += 2
        if moving_left:
            player_movement[0] -= 2
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3

        # Relacionando o jogador e o mapa
        player_rect, collisions = move(player_rect, player_movement, tile_rect)

        # Mantém o personagem colidindo com o chão
        if collisions['bottom'] or collisions['top']:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1

        # Põe o personagem na tela
        display.blit(player_image, (player_rect.x, player_rect.y))

        # Apurando eventos
        for event in pg.event.get():
            x, y = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                game_exit = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if timer == 0:
                        timer = 0.001
                    elif timer < 0.2:
                        if air_timer < 6:
                            vertical_momentum = -5
                            timer = 0
                    if x > win_size[0] / 2:
                        moving_right = True
                    if x < win_size[0] / 2:
                        moving_left = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if x > win_size[0] / 2:
                        moving_right = False
                    if x < win_size[0] / 2:
                        moving_left = False

        # Timer pro double click
        if timer != 0:
            timer += dt
            if timer >= 0.2:
                timer = 0
        dt = clock.tick(60) / 1000

        # Mostrando para o usuário e FPS
        screen.blit(pg.transform.scale(display, win_size), (0, 0))
        pg.display.update()


# game_intro()
game_loop()
pg.quit()
sys.exit()
