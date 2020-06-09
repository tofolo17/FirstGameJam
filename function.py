import pygame as pg


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


animation_frames = {}  # Frames das animações


# Checando as animações nas pastas e alocando-as em listas
def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pg.image.load(img_loc).convert()
        animation_image.set_colorkey((0, 114, 188))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


# Transição entre animações
def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


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
def blit_arrow(x_a, y_a, angle_a, opacity_a, obj, window):
    obj.set_alpha(opacity_a)
    window.blit(pg.transform.rotate(obj, angle_a), (x_a, y_a))


# Efeito Parallax
def bg_moving(x_bg, bg_layer, h, window, w_width):
    rel_x = x_bg % bg_layer.get_rect().width
    window.blit(bg_layer, (rel_x - bg_layer.get_rect().width, h))
    if rel_x < w_width:
        window.blit(bg_layer, (rel_x, h))


def un_bug_collided_bg(x1, x2, x3, right, left):
    if right:
        x1 += 0.5
        x2 += 0.3
        x3 += 0.15
    if left:
        x1 -= 0.5
        x2 -= 0.3
        x3 -= 0.15


def change_img_conditional(component, values: list, def_result):
    i = 0
    while i < len(values) and component < 8:
        if values[i] <= component < values[i+1]:
            image_n = def_result + i
            return image_n
        i += 1
