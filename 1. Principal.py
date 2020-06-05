import os
import sys
from random import randint

import pygame as pg

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centralizando

pg.init()  # Inicializando o Pygame

# Tamanho da tela e título
win_size = [800, 600]  # pg.display.Info().current_w - 5, pg.display.Info().current_h - 40
screen = pg.display.set_mode(size=win_size)
pg.display.set_caption('Rocket Wave')
display = pg.Surface((300, 200))
clock = pg.time.Clock()

true_scroll = [0, 0]  # Variável para o seguir da câmera


# Carregando o mapa
def load_map(path):
    file = open(path + '.txt', 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


# Variáveis do mapa
level_map = load_map('mapfile')
full_block = pg.image.load('Imagens/block_1.png')
half_block = pg.image.load('Imagens//block_2.png')
half_block_vertical = pg.image.load('Imagens//block_3.png')
half_block_right = pg.image.load('Imagens//block_4.png')
half_block_left = pg.image.load('Imagens//block_5.png')
half_support_right = pg.image.load('Imagens//block_6.png')
half_support_left = pg.image.load('Imagens//block_7.png')
glass = pg.image.load('Imagens//block_8.png')
chimney = pg.image.load('Imagens//block_9.png')
antenna = pg.image.load('Imagens//block_10.png')


# Testa lugares colidíveis
def collision_test(rect, tiles):
    hit_list = []
    for each_tile in tiles:
        if rect.colliderect(each_tile):
            hit_list.append(each_tile)
    return hit_list


# Detectando movimentos e colisões
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += int(movement[0])
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        if movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += int(movement[1])
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


# Colocando imagens opacas na tela
def blit_arrow(x_a, y_a, angle_a, opacity_a, obj):
    obj.set_alpha(opacity_a)
    display.blit(pg.transform.rotate(obj, angle_a), (x_a, y_a))


# Efeito Parallax
def bg_moving(x_bg, bg_layer, h):
    rel_x = x_bg % bg_layer.get_rect().width
    display.blit(bg_layer, (rel_x - bg_layer.get_rect().width, h))
    if rel_x < win_size[0]:
        display.blit(bg_layer, (rel_x, h))


# Loop principal
def game_loop():

    # Variáveis do loop
    game_exit = moving_left = moving_right = False

    # Variáveis físicas
    vertical_momentum = air_timer = speed_timer = dt = 0
    permitted_vm = [0, 0.3, 0.6, 0.8999999999999999, 1.2, 1.5]
    stars_speed = 0.3

    # Variáveis da opacidade
    op_r_a = op_l_a = op_u_a = op_ur_a = op_ul_a = 70

    # Variáveis das setas
    arrow = pg.image.load('Imagens//seta.png').convert_alpha()
    arrow.set_colorkey((255, 255, 255))

    # Variáveis do personagem
    player_image = pg.image.load('Imagens//player.png').convert()
    player_image.set_colorkey((255, 255, 255))
    player_rect = pg.Rect(100, 116, 5, 13)

    # Objetos do fundo
    x_layer1 = x_layer2 = x_layer3 = 0
    background = pg.image.load("Imagens//bg.png")
    buildings1 = pg.image.load("Imagens//layer1.png")
    buildings2 = pg.image.load("Imagens//layer2.png")
    buildings3 = pg.image.load("Imagens//layer3.png")
    stars = []
    for n in range(35):
        stars.append([randint(0, 300), randint(0, 90)])

    # Convertendo elementos da matriz em blocos
    def displaying_tile(block_name, w, h, n_block, corrector_x, corrector_y, collide=0):
        if tile == f'{n_block}':
            display.blit(block_name, (x * 16 + scroll[0] - corrector_x, y * 16 + scroll[1] + corrector_y))
            if not collide:
                tile_rect.append(pg.Rect(x * 16, y * 16, w, h))

    # Enquanto o jogo estiver aberto...
    while not game_exit:

        display.fill((0, 0, 0))  # Preenchendo a tela com algo
        display.blit(background, (0, 0))  # Fundo gradiente

        # Movimentação das construções
        bg_moving(x_layer3, buildings3, 95)
        bg_moving(x_layer2, buildings2, 85)
        bg_moving(x_layer1, buildings1, 100)

        # Câmera
        true_scroll[0] -= ((player_rect.x + true_scroll[0]) - 152) / 12
        true_scroll[1] -= ((player_rect.y + true_scroll[1]) - 140) / 12
        scroll = true_scroll.copy()
        scroll[0] = int(true_scroll[0])
        scroll[1] = int(true_scroll[1])

        # Adiciona as estrelas ao céu
        for star in stars:
            pg.draw.line(display, (255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[0] = star[0] - stars_speed
            if star[0] < 0:
                star[0] = 300
                star[1] = randint(0, 90)

        # Construção do mapa
        tile_rect = []
        y = 0
        for layer in level_map:
            x = 0
            for tile in layer:
                displaying_tile(full_block, 16, 16, 1, 0, 0)
                displaying_tile(half_block, 16, 4, 2, 0, 0)
                displaying_tile(half_block_vertical, 4, 16, 3, 6, 0)
                displaying_tile(half_block_right, 16, 4, 4, 0, 0)
                displaying_tile(half_block_left, 16, 4, 5, 0, 0)
                displaying_tile(half_support_right, 16, 16, 6, 0, 0)
                displaying_tile(half_support_left, 16, 16, 7, 0, 0)
                displaying_tile(glass, 16, 16, 8, 0, 0)
                displaying_tile(chimney, 10, 10, 9, 0, 7, True)
                displaying_tile(antenna, 84, 96, 10, 0, -76, True)
                x += 1
            y += 1

        # Movimento do personagem
        player_movement = [0, 0]
        if (speed_timer > 0.8) and vertical_momentum in permitted_vm:
            speed_boost = 3
        else:
            speed_boost = 2
        if moving_right:
            speed_timer += dt
            player_movement[0] += speed_boost
            stars_speed = 0.4
            x_layer1 -= 0.5
            x_layer2 -= 0.3
            x_layer3 -= 0.15
        elif moving_left:
            speed_timer += dt
            player_movement[0] -= speed_boost
            stars_speed = 0.2
            x_layer1 += 0.5
            x_layer2 += 0.3
            x_layer3 += 0.15
        else:
            speed_timer = 0
            stars_speed = 0.3
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.3
        if vertical_momentum > 5:
            vertical_momentum = 5

        # Relacionando o jogador e o mapa
        player_rect, collisions = move(player_rect, player_movement, tile_rect)

        # Não deixa a tela se mexer quando colidido com a parede
        if collisions['right']:
            x_layer1 += 0.5
            x_layer2 += 0.3
            x_layer3 += 0.15
        if collisions['left']:
            x_layer1 -= 0.5
            x_layer2 -= 0.3
            x_layer3 -= 0.15

        # Mantém o personagem colidindo com o chão
        if collisions['bottom']:
            air_timer = vertical_momentum = 0
        else:
            air_timer += 1

        # Põe o personagem e as setas na tela
        display.blit(player_image, (player_rect.x + scroll[0], player_rect.y + scroll[1]))
        blit_arrow(41, 100, 180, op_l_a, arrow)
        blit_arrow(225, 35, 45, op_ur_a, arrow)
        blit_arrow(41, 35, 135, op_ul_a, arrow)
        blit_arrow(141, 35, 90, op_u_a, arrow)
        blit_arrow(225, 100, 0, op_r_a, arrow)

        x, y = pg.mouse.get_pos()  # Pegando as coordenadas do mouse
        # Movimentos em X
        if x > (2 / 3 * win_size[0]) and (y > win_size[1] / 6):
            moving_left = False
            moving_right = True
            op_r_a = 100
        elif x < win_size[0] / 3 and (y > win_size[1] / 6):
            moving_right = False
            moving_left = True
            op_l_a = 100
        else:
            moving_right = moving_left = False
            op_r_a = op_l_a = op_u_a = op_ur_a = op_ul_a = 70

        # Movimentos em Y
        if (y < win_size[1] / 3) and (y > win_size[1] / 6) and air_timer < 8:
            op_u_a = 100
            if collisions['top']:
                vertical_momentum = -1
            elif collisions['bottom']:
                vertical_momentum = -6
                collisions['top'] = True
        elif collisions['bottom']:
            op_u_a = op_ul_a = op_ur_a = 70

        # Analisando opacidade das setas diagonais
        if op_u_a == 100 and op_r_a == 100:
            op_ur_a = 100
        elif op_u_a == 100 and op_l_a == 100:
            op_ul_a = 100
        else:
            op_ul_a = 70

        # Morte do personagem
        if air_timer > 80:
            game_exit = True

        # Apurando eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True

        # Update da tela e FPS
        screen.blit(pg.transform.scale(display, win_size), (0, 0))
        pg.display.update()
        dt = clock.tick(60) / 1000


game_loop()
pg.quit()
sys.exit()
