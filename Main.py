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

# Variável para o seguir da câmera
true_scroll = [0, 0]


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


level_map = load_map('mapfile')

grass_img = pg.image.load('Imagens//grass.png')
dirt_img = pg.image.load('Imagens//dirt.png')


# Testa lugares colidíveis
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
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


# Colocando superfícies opacas na tela
def surface_and_opacity(color, width, height, x_pos, y_pos, opacity):
    colored_surface = pg.Surface((width, height))
    pg.Surface.fill(colored_surface, color)
    colored_surface.set_alpha(opacity)
    screen.blit(colored_surface, (x_pos, y_pos))


# Colocando imagens opacas na tela
def blit_arrow(x_a, y_a, angle_a, opacity_a, obj):
    obj.set_alpha(opacity_a)
    display.blit(pg.transform.rotate(obj, angle_a), (x_a, y_a))


# Loop principal
def game_loop():
    # Variáveis do loop
    game_exit = moving_left = moving_right = False

    # Variáveis físicas
    vertical_momentum = air_timer = speed_timer = dt = 0
    permitted_vm = [0, 0.3, 0.6, 0.8999999999999999, 1.2]

    # Variáveis da opacidade
    op_r_a = op_l_a = op_u_a = op_ur_a = op_ul_a = 40
    op_r_bg = op_l_bg = op_u_bg = op_ur_bg = op_ul_bg = 20

    # Variáveis do personagem e da seta
    arrow = pg.image.load('Imagens//seta.png').convert_alpha()
    arrow.set_colorkey((255, 255, 255))
    player_image = pg.image.load('Imagens//player.png').convert()
    player_image.set_colorkey((255, 255, 255))
    player_rect = pg.Rect(100, 100, 5, 13)

    # Objetos do fundo
    background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]],
                          [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

    # Enquanto o jogo estiver aberto...
    while not game_exit:

        display.fill((146, 244, 255))  # Cor de fundo

        # Câmera
        true_scroll[0] -= ((player_rect.x + true_scroll[0]) - 152) / 10
        true_scroll[1] -= ((player_rect.y + true_scroll[1]) - 106) / 10
        scroll = true_scroll.copy()
        scroll[0] = int(true_scroll[0])
        scroll[1] = int(true_scroll[1])

        # Construção do fundo
        pg.draw.rect(display, (7, 80, 75), pg.Rect(0, 120, 300, 80))
        for background_object in background_objects:
            obj_rect = pg.Rect(int(background_object[1][0] + true_scroll[0] * background_object[0]),
                               int(background_object[1][1] + true_scroll[1] * background_object[0]),
                               int(background_object[1][2]),
                               int(background_object[1][3]))
            if background_object[0] == 0.5:
                pg.draw.rect(display, (14, 222, 150), obj_rect)
            else:
                pg.draw.rect(display, (9, 91, 85), obj_rect)

        # Construção do mapa
        tile_rect = []
        y = 0
        for layer in level_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirt_img, (x * 16 + scroll[0], y * 16 + scroll[1]))
                if tile == '2':
                    display.blit(grass_img, (x * 16 + scroll[0], y * 16 + scroll[1]))
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
        elif moving_left:
            speed_timer += dt
            player_movement[0] -= speed_boost
        else:
            speed_timer = 0
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.3
        if vertical_momentum > 5:
            vertical_momentum = 5

        # Relacionando o jogador e o mapa
        player_rect, collisions = move(player_rect, player_movement, tile_rect)

        # Mantém o personagem colidindo com o chão
        if collisions['bottom']:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1

        # Põe o personagem e as setas na tela
        display.blit(player_image, (player_rect.x + scroll[0], player_rect.y + scroll[1]))
        blit_arrow(41, 100, 180, op_l_a, arrow)
        blit_arrow(225, 35, 45, op_ur_a, arrow)
        blit_arrow(41, 35, 135, op_ul_a, arrow)
        blit_arrow(141, 35, 90, op_u_a, arrow)
        blit_arrow(225, 100, 0, op_r_a, arrow)

        x, y = pg.mouse.get_pos()
        # Movimentos em X
        if x > (2 / 3 * win_size[0]) and (y > win_size[1] / 6):
            moving_left = False
            moving_right = True
            op_r_a = 70
            op_r_bg = 50
        elif x < win_size[0] / 3 and (y > win_size[1] / 6):
            moving_right = False
            moving_left = True
            op_l_a = 70
            op_l_bg = 50
        else:
            moving_right = moving_left = False
            op_r_a = op_l_a = op_u_a = op_ur_a = op_ul_a = 40
            op_r_bg = op_l_bg = op_u_bg = op_ur_bg = op_ul_bg = 20

        # Movimentos em Y
        if (y < win_size[1] / 3) and (y > win_size[1] / 6) and air_timer < 10:
            op_u_a = 70
            op_u_bg = 50
            if collisions['top']:
                vertical_momentum = -1
            elif collisions['bottom']:
                vertical_momentum = -6
                collisions['top'] = True
        elif collisions['bottom']:
            op_u_a = op_ul_a = op_ur_a = 40
            op_u_bg = op_ul_bg = op_ur_bg = 20

        # Analisando opacidade das setas horizontais
        if op_u_a == 70 and op_r_a == 70:
            op_ur_bg = op_ur_a = 50
        elif op_u_a == 70 and op_l_a == 70:
            op_ul_bg = op_ul_a = 50
        else:
            op_ul_bg = op_ul_a = 20

        # Apurando eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True

        # Update da tela, superfícies de movimento e FPS
        screen.blit(pg.transform.scale(display, win_size), (0, 0))
        surface_and_opacity((214, 107, 0), int(win_size[0] / 3), int(4 / 6 * win_size[1]),
                            0, int(win_size[1] / 3), op_l_bg)
        surface_and_opacity((214, 107, 0), int(win_size[0] / 3), int(4 / 6 * win_size[1]),
                            int(2 / 3 * win_size[0]), int(win_size[1] / 3), op_r_bg)
        surface_and_opacity((214, 107, 0), int(win_size[0] / 3 + 1), int(win_size[1] / 6),
                            int(win_size[0] / 3), int(win_size[1] / 6), op_u_bg)
        surface_and_opacity((214, 107, 0), int(win_size[0] / 3), int(win_size[1] / 6),
                            0, int(win_size[1] / 6), op_ul_bg)
        surface_and_opacity((214, 107, 0), int(win_size[0] / 3), int(win_size[1] / 6),
                            int(2 * win_size[0] / 3), int(win_size[1] / 6), op_ur_bg)
        pg.display.update()
        dt = clock.tick(60) / 1000


game_loop()
pg.quit()
sys.exit()
