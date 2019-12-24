import os
import pygame
from Unique_Heroes import Hero

pygame.init()

width = 1200
height = 1000
size = width, height
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


clock = pygame.time.Clock()
FPS = 30



# Загрузка изображения
def load_image(name, colorkey=None):
    name = name + '/' + name + '_bg.png'
    fullname = os.path.join('data/lvls/', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Загрузка уровней
def load_level(filename):
    filename = filename + '/' + filename + '_bg.txt'
    filename = "data/lvls/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('1'), Травой
    return list(map(lambda x: x.ljust(max_width, '1'), level_map))


class BackGround(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprite)
        bg_im = load_image('debug1')
        self.image = pygame.transform.scale(bg_im, (3840, 3840))
        self.rect = self.image.get_rect()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def generate_level():
    return BackGround()

all_sprite = pygame.sprite.Group()

static_bg = generate_level()
camera = Camera()

running = 1
while running:
    all_sprite.draw(screen)
    pygame.display.flip()
    for sprite in all_sprite:
        camera.apply(sprite)

    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] >= width - 10:
        camera.dx += 1
    elif mouse_pos[1] <= 10:
        camera.dy -= 1
    elif mouse_pos[0] <= 10:
        camera.dx -= 1
    elif mouse_pos[1] >= height - 10:
        camera.dy += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

    #camera.dx = 0
    #camera.dy = 0

    clock.tick(FPS)




