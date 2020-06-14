import os
import sys
from random import randint, choice
from function import *

import pygame as pg

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centralizando

pg.init()  # Inicializando o Pygame

# Tamanho da tela e título
win_size = [900, 600]  # pg.display.Info().current_w - 5, pg.display.Info().current_h - 40
screen = pg.display.set_mode(size=win_size)
pg.display.set_caption('Rocket Wave')
display = pg.Surface((600, 400))
clock = pg.time.Clock()

# Variáveis do mapa
level_map = load_map('mapfile')
full_block = pg.image.load('Imagens/block_1.png')
half_block = pg.image.load('Imagens/block_2.png')
half_block_vertical = pg.image.load('Imagens/block_3.png')
half_block_right = pg.image.load('Imagens/block_4.png')
half_block_left = pg.image.load('Imagens/block_5.png')
half_support_right = pg.image.load('Imagens/block_6.png')
half_support_left = pg.image.load('Imagens/block_7.png')
glass = pg.image.load('Imagens/block_8.png')
chimney = pg.image.load('Imagens/block_9.png')
antenna = pg.image.load('Imagens/block_10.png')

# Dicionário que guarda as informações sobre as animações
animation_database = {'idle': load_animation('Player Animations/idle', [7, 7, 7, 7]),
                      'run': load_animation('Player Animations/run', [7, 7, 7, 7, 7, 7, 7, 7]),
                      'jump': load_animation('Player Animations/jump', [7, 7, 7, 7, 7, 7, 7]),
                      'shoot': load_animation('Player Animations/shoot', [3, 3, 3, 3]),
                      'walkshoot': load_animation('Player Animations/walkshoot', [4, 4, 4, 4, 4, 4, 4, 4]),
                      'jumpshoot': load_animation('Player Animations/jumpshoot', [3, 3, 3, 3])}


# Loop principal
def game_loop():
    # Variáveis do loop
    game_exit = moving_left = moving_right = False
    true_scroll = [0, 0]

    # Variáveis da trocação
    shoot = False
    bullets, shoot_pos = [], []
    n_of_bullets = time_to_shoot = time_to_recharge = 0
    bullet_img = pg.image.load('Imagens/bullet.png')

    # Variáveis físicas
    vertical_momentum = air_timer = speed_timer = charge_timer = dt = 0
    permitted_vm = [0, 0.3, 0.6, 0.8999999999999999, 1.2, 1.5]
    stars_speed = 0.3
    time_to_use = 8

    # Variáveis da opacidade
    right_arrow_opacity = left_arrow_opacity = upper_arrow_opacity = up_right_arrow_opacity = up_left_arrow_opacity \
        = super_arrow_opacity = 70

    # Variáveis das setas
    arrow = pg.image.load('Imagens//seta.png').convert_alpha()
    img_arrow_n = 5

    # Variáveis do personagem
    player_rect = pg.Rect(100, 100, 25, 30)
    player_frame = image_offset = 0
    player_action = 'idle'
    player_flip = False

    # Objetos do fundo
    x_building1 = x_building2 = x_building3 = 0
    background = pg.image.load('Imagens/bg.png')
    buildings1 = pg.image.load('Imagens/layer1.png')
    buildings2 = pg.image.load('Imagens/layer2.png')
    buildings3 = pg.image.load('Imagens/layer3.png')
    stars = []
    for n in range(45):
        stars.append([randint(0, 600), randint(0, 140)])

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

        # Câmera
        true_scroll[0] -= ((player_rect.x + true_scroll[0]) - 230) / 12
        true_scroll[1] -= ((player_rect.y + true_scroll[1]) - 250) / 12
        scroll = true_scroll.copy()
        scroll[0] = int(true_scroll[0])
        scroll[1] = int(true_scroll[1])

        # Movimentação das construções
        bg_moving(x_building3, buildings3, 140 + scroll[1] / 8, display, win_size[0])
        bg_moving(x_building2, buildings2, 140 + scroll[1] / 6, display, win_size[0])
        bg_moving(x_building1, buildings1, 165 + scroll[1] / 4, display, win_size[0])

        # Adiciona as estrelas ao céu
        for star in stars:
            pg.draw.line(display, (255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[0] = star[0] - stars_speed
            if star[0] < 0:
                star[0] = 600
                star[1] = randint(0, 140)

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
        if speed_timer > 0.8 and vertical_momentum in permitted_vm:
            speed_boost = 3
        else:
            speed_boost = 2
        if moving_right:
            player_movement[0] += speed_boost
            player_flip = False
            speed_timer += dt
            stars_speed = 0.4
            x_building1 -= 0.5
            x_building2 -= 0.3
            x_building3 -= 0.15
        elif moving_left:
            player_movement[0] -= speed_boost
            player_flip = True
            speed_timer += dt
            stars_speed = 0.2
            x_building1 += 0.5
            x_building2 += 0.3
            x_building3 += 0.15
        else:
            stars_speed = 0.3
            speed_timer = 0
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.3
        if vertical_momentum > 7:
            vertical_momentum = 7

        # Animações baseadas no movimento
        if moving_left or moving_right:
            if shoot and time_to_recharge < 0:
                if air_timer <= 5:
                    player_action, player_frame = change_action(player_action, player_frame, 'walkshoot')
                else:
                    player_action, player_frame = change_action(player_action, player_frame, 'jumpshoot')
            elif air_timer > 5:
                player_action, player_frame = change_action(player_action, player_frame, 'jump')
            else:
                player_action, player_frame = change_action(player_action, player_frame, 'run')
        else:
            if shoot and time_to_recharge < 0:
                if air_timer <= 5:
                    player_action, player_frame = change_action(player_action, player_frame, 'shoot')
                else:
                    player_action, player_frame = change_action(player_action, player_frame, 'jumpshoot')
            elif air_timer > 5:
                player_action, player_frame = change_action(player_action, player_frame, 'jump')
            else:
                player_action, player_frame = change_action(player_action, player_frame, 'idle')

        player_rect, collisions = move(player_rect, player_movement, tile_rect)  # Relacionando o jogador e o mapa

        # Não deixa a tela se mexer quando colidido com a parede
        un_bug_collided_bg(x_building1, x_building2, x_building3, collisions['right'], collisions['left'])

        # Mantém o personagem colidindo com o chão
        if collisions['bottom']:
            air_timer = vertical_momentum = 0
        else:
            air_timer += 1

        # Transição entre os frames armazenados
        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = animation_frames[player_img_id]
        display.blit(pg.transform.flip(player_img, player_flip, False),
                     (player_rect.x - player_img.get_width()/2 + scroll[0] + image_offset, player_rect.y + scroll[1]))

        # Colocando as setas na tela
        rocket_arrow = pg.image.load(f'Imagens/superarrow_{img_arrow_n}.png').convert_alpha()
        blit_arrow(50, 200, 180, left_arrow_opacity, arrow, display)
        blit_arrow(482, 70, 45, up_right_arrow_opacity, arrow, display)
        blit_arrow(50, 70, 135, up_left_arrow_opacity, arrow, display)
        blit_arrow(279, 70, 90, upper_arrow_opacity, arrow, display)
        blit_arrow(492, 200, 0, right_arrow_opacity, arrow, display)
        blit_arrow(279, 300, 90, super_arrow_opacity, rocket_arrow, display)

        x, y = pg.mouse.get_pos()  # Pegando as coordenadas do mouse
        # Movimentos em X
        if x > (2 / 3 * win_size[0]) and (y > win_size[1] / 6):
            moving_left = False
            moving_right = True
            right_arrow_opacity = 100
        elif x < win_size[0] / 3 and (y > win_size[1] / 6):
            moving_right = False
            moving_left = True
            left_arrow_opacity = 100
        else:
            moving_right = moving_left = False
            right_arrow_opacity = left_arrow_opacity = upper_arrow_opacity = up_right_arrow_opacity = \
                up_left_arrow_opacity = super_arrow_opacity = 70

        # Movimentos em Y
        if (y < win_size[1] / 3) and (y > win_size[1] / 6) and air_timer < 8:
            if collisions['top']:
                vertical_momentum = -1
            elif collisions['bottom']:
                vertical_momentum = -6
                collisions['top'] = True
        elif collisions['bottom']:
            upper_arrow_opacity = up_left_arrow_opacity = up_right_arrow_opacity = 70
        if y > 4 * win_size[1] / 5:
            charge_timer += dt
            if vertical_momentum in permitted_vm and time_to_use >= 8:
                super_arrow_opacity = 150
                player_rect.x += choice([-1.25, 1, -0.5, 0, 0.5, 1, 1.25])
            if charge_timer > 1:
                vertical_momentum = -12
                charge_timer = time_to_use = 0
        else:
            charge_timer = 0

        # Analisando opacidade das setas diagonais e verticais
        if vertical_momentum not in permitted_vm:
            upper_arrow_opacity = 100
        if upper_arrow_opacity == 100 and right_arrow_opacity == 100:
            up_right_arrow_opacity = 100
        elif upper_arrow_opacity == 100 and left_arrow_opacity == 100:
            up_left_arrow_opacity = 100
        else:
            up_left_arrow_opacity = 70
        if time_to_use >= 8:
            time_to_use = 8
            img_arrow_n = 5
        else:
            img_arrow_n = change_img_conditional(time_to_use, [0, 2, 4, 6, 8], 1)
            charge_timer = 0

        # Apurando eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player_flip:
                        image_offset = -3
                    else:
                        image_offset = 2
                    shoot = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    image_offset = 0
                    shoot = False

        time_to_recharge -= dt  # Tempo para conseguir atirar
        # Balas
        if shoot and time_to_recharge < 0:
            player_movement[0] = 100
            time_to_shoot += dt
            if len(bullets) == 0:
                initial_bullet = 0
            else:
                initial_bullet = 0.2
            while n_of_bullets <= 30 and time_to_shoot > initial_bullet:
                bullets.append([player_rect.x, player_rect.y])
                shoot_pos.append([player_flip])
                time_to_shoot = 0
                n_of_bullets += 1
                if n_of_bullets > 30:
                    time_to_recharge = 2
                    n_of_bullets = 0
                    shoot = False
        for bullet in bullets:
            pos = bullets.index(bullet)
            if not shoot_pos[pos][0]:
                bullet[0] += 15
                x_start_shoot = 10
                angle = 0
            else:
                bullet[0] -= 15
                x_start_shoot = 0
                angle = 180
            display.blit(pg.transform.rotate(bullet_img, angle),
                         (bullet[0] + x_start_shoot + scroll[0], bullet[1] + 14 + scroll[1]))
            if bullet[0] > player_rect.x + 300 + arrow.get_width() or \
                    bullet[0] < player_rect.x - 300 - arrow.get_width():
                bullets.remove(bullet)
                shoot_pos.remove(shoot_pos[pos])

        # Morte do personagem
        if air_timer > 120:
            game_exit = True

        # Update da tela e FPS
        screen.blit(pg.transform.scale(display, win_size), (0, 0))
        pg.display.update()
        time_to_use += dt
        dt = clock.tick(60) / 1000


game_loop()
pg.quit()
sys.exit()
