import pygame
import os

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('generatorFiles', name)
    image = pygame.image.load(fullname).convert()
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
GRAY = pygame.Color('gray')
GREEN = pygame.Color('green')
BROWN = pygame.Color('brown')
SWAMPY = (172, 183, 142)
MINT = (127, 255, 212)


class Cell(pygame.sprite.Sprite):
    def __init__(self, penalty, able_to_go, sprite, xy=None, wh=None):
        self.penalty = penalty
        self.able_to_go = able_to_go
        self.sprite = sprite
        self.xy = xy
        self.wh = wh


class Snow(Cell):  # 0
    def __init__(self):
        super().__init__(4, True, WHITE, wh=(1, 1))
        self.damage = 0.1


class Swamp(Cell):  # 1
    def __init__(self):
        super().__init__(4, True, SWAMPY)


class Road(Cell):  # 2
    def __init__(self):
        super().__init__(1, True, GRAY)


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
    def __init__(self):
        super().__init__(0, True, GRAY, wh=(2, 2))
