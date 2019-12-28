import pygame
import os

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('generatorFiles', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Цвета
RED = pygame.Color('red')
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
BLUE = pygame.Color('blue')
GAY = pygame.Color('gray')
GREEN = pygame.Color('green')
BROWN = pygame.Color('brown')
SWAMPY = (172, 183, 142)
MINT = (127, 255, 212)


class Cell(pygame.sprite.Sprite):
    def __init__(self, penalty, able_to_go, sprite, xy=None, wh=None):
        super().__init__()
        self.penalty = penalty
        self.able_to_go = able_to_go
        self.sprite = sprite
        self.xy = xy
        self.wh = wh


class Snow(Cell):  # 0
    def __init__(self, xy):
        super().__init__(4, True, WHITE, wh=(1, 1), xy=None)
        self.damage = 0.1


class Swamp(Cell):  # 1
    def __init__(self):
        super().__init__(4, True, SWAMPY)


class Road(Cell):  # 2
    def __init__(self):
        super().__init__(1, True, GAY)


class Water(Cell):  # 3
    def __init__(self):
        super().__init__(2, False, BLUE)


class Mountain(Cell):  # 4
    def __init__(self):
        super().__init__(0, False, BROWN)


class Forest(Cell):  # 5
    def __init__(self):
        super().__init__(0, False, MINT)


class Castle(Cell):
    def __init__(self, xy=None):
        super().__init__(0, True, GAY, wh=(2, 2))
        self.image = load_image("castle.png", colorkey=-1)
        self.image = pygame.transform.scale(self.image, (self.wh[0] * 30, self.wh[1] * 30))
        self.rect = self.image.get_rect()
        self.rect.x = xy[0]
        self.rect.y = xy[1]

