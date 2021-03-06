import pygame


def load_image(path):
    surf = pygame.image.load(path)
    surf.set_colorkey(surf.get_at((0, 0)))
    return surf


class Unit:
    def __init__(self, name, count, price, image, speed):
        self.name = name
        self.count = count
        self.price = price
        self.image = image
        self.speed = speed

# Армия нежити
class Skeleton(Unit):
    def __init__(self, count):
        super().__init__('Скелеты', count, 60, load_image('data\\UNITS_SPRYTE\\Skeleton.png'), 6)


class Zombie(Unit):
    def __init__(self, count):
        super().__init__('Зомби', count, 80, load_image('data\\UNITS_SPRYTE\\Zombi.png'), 4)


class Leach(Unit):
    def __init__(self, count):
        super().__init__("Личи", count, 160, load_image('data\\UNITS_SPRYTE\\Leach.png'), 5)


# class HorsemanOfTheApocalypse(Unit):
#     def __init__(self, count):
#         super().__init__(count, 250)
#
#
# class NecroMancer(Unit):
#     def __init__(self, count):
#         super().__init__(count, 300)


# Армия людей

# Армия людей
class SpearMan(Unit):
    def __init__(self, count):
        super().__init__("Копейщики", count, 60, load_image('data\\UNITS_SPRYTE\\Spearman.png'), 7)


class Archer(Unit):
    def __init__(self, count):
        super().__init__("Лучники", count, 100, load_image('data\\UNITS_SPRYTE\\Archer.png'), 3)


class Cavalryman(Unit):
    def __init__(self, count):
        super().__init__("Конники", count, 250, load_image('data\\UNITS_SPRYTE\\Cavalryman.png'), 14)