import os
import sys
from random import randint

import pygame as pg

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centralizando

pg.init()  # Inicializando o Pygame

# Tamanho da tela e título
win_size = [500, 400]  # pg.display.Info().current_w - 5, pg.display.Info().current_h - 40
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
test_block = pg.image.load('Imagens/block.png')


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


# Loop principal
def game_loop():
    # Variáveis do loop
    game_exit = moving_left = moving_right = False

    # Variáveis físicas
    vertical_momentum = air_timer = speed_timer = dt = x_bg = 0
    permitted_vm = [0, 0.3, 0.6, 0.8999999999999999, 1.2, 1.5]
    stars_speed = 0.35

    # Variáveis da opacidade
    op_r_a = op_l_a = op_u_a = op_ur_a = op_ul_a = 70

    # Variáveis das setas
    arrow = pg.image.load('Imagens//seta.png').convert_alpha()
    arrow.set_colorkey((255, 255, 255))

    # Variáveis do personagem
    player_image = pg.image.load('Imagens//player.png').convert()
    player_image.set_colorkey((255, 255, 255))
    player_rect = pg.Rect(100, 100, 5, 13)

    # Objetos do fundo
    background = pg.image.load("Imagens//bg.png")
    buildings1 = pg.image.load("Imagens//layer1.png")
    stars = []
    for n in range(40):
        stars.append([randint(0, 300), randint(0, 80)])

    # Enquanto o jogo estiver aberto...
    while not game_exit:

        display.fill((0, 0, 0))  # Preenchendo a tela com algo
        display.blit(background, (0, 0))  # Fundo gradiente

        # Movimentação das construções
        rel_x = x_bg % buildings1.get_rect().width
        display.blit(buildings1, (rel_x - background.get_rect().width, 99))
        if rel_x < win_size[0]:
            display.blit(buildings1, (rel_x, 99))
        if moving_right:
            x_bg -= 0.5
        elif moving_left:
            x_bg += 0.5

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
                star[1] = randint(0, 80)

        # Construção do mapa
        tile_rect = []
        y = 0
        for layer in level_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(test_block, (x * 16 + scroll[0], y * 16 + scroll[1]))
                if tile != '0':
                    tile_rect.append(pg.Rect(x * 16, y * 16, 16, 16))
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
            stars_speed = 0.45
        elif moving_left:
            speed_timer += dt
            player_movement[0] -= speed_boost
            stars_speed = 0.25
        else:
            speed_timer = 0
            stars_speed = 0.35
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.3
        if vertical_momentum > 5:
            vertical_momentum = 5

        # Relacionando o jogador e o mapa
        player_rect, collisions = move(player_rect, player_movement, tile_rect)

        # Não deixa a tela se mexer quando colidido com a parede
        if not collisions['right']:
            x_bg = x_bg
        else:
            x_bg += 0.5
        if not collisions['left']:
            x_bg = x_bg
        else:
            x_bg -= 0.5

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

        # Update da tela, superfícies de movimento e FPS
        screen.blit(pg.transform.scale(display, win_size), (0, 0))
        pg.display.update()
        dt = clock.tick(60) / 1000


game_loop()
pg.quit()
sys.exit()
