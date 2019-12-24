import pygame

pygame.init()

# Настройка экрана
WIDTH = 1080
HEIGHT = 1080
SIZE = WIDTH, HEIGHT
SCREEN = pygame.display.set_mode(SIZE)

# Цвета
RED = pygame.Color('red')
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
BLUE = pygame.Color('blue')
GRAY = pygame.Color('gray')
GREEN = pygame.Color('green')
BROWN = pygame.Color('brown')
SWAMPY = pygame.Color((172, 183, 142))
MINT = pygame.Color((127, 255, 212))


class Cell(pygame.sprite.Sprite):
    def __init__(self, penalty, able_to_go, sprite):
        self.penalty = penalty
        self.able_to_go = able_to_go
        self.sprite = sprite


class Grass(Cell):  # 1
    def __init__(self):
        super().__init__(2, True, GREEN)


class Snow(Cell):  # 2
    def __init__(self):
        super().__init__(4, True, WHITE)
        self.damage = 10  # это проценты


class Swamp(Cell):  # 3
    def __init__(self):
        super().__init__(4, True, SWAMPY)


class Road(Cell):  # 4
    def __init__(self):
        super().__init__(1, True, GRAY)


class Water(Cell):  # 5
    def __init__(self):
        super().__init__(2, False, BLUE)


class Mountain(Cell):  # 6
    def __init__(self):
        super().__init__(0, False, BROWN)


class Forest(Cell):  # 7
    def __init__(self):
        super().__init__(0, False, MINT)