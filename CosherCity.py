import pygame
from UnitTypes import *




pygame.init()

width = 1200
height = 1000
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Город нежити')


# хранит параметры, для отрисовки окон и окошек
class City:
    def __init__(self):
        # Разные статусы, благодаря которым происходит отрисовка
        self.panorama = 0
        self.buy_unit = 1
        self.buy_hero = 2
        self.upgrade_city = 3
        self.unit = None    # Заглушка


        self.interface_down_surf = self.load_sprite("data\ALL_CITIES_SPRYTES\interface_down", '', 0)
        self.buy_unit_surf = self.load_sprite('data\ALL_CITIES_SPRYTES\interface_buy_unit', '', 0)
        self.buy_hero_surf = self.load_sprite('data\ALL_CITIES_SPRYTES\\interface_buy_hero', '', 0)
        self.active = self.panorama

    def draw_buy_unit_window(self, unit):
        screen.blit(self.buy_unit_surf, (164, 143))

    def draw_buy_hero_window(self, hero1, hero2):
        screen.blit(self.buy_hero_surf, (247, 48))

    def load_sprite(self, path, obj, check):
        if check:
            surf = pygame.image.load(path + str(obj) + '.png')
            surf.set_colorkey(surf.get_at((0, 0)))
        else:
            surf = pygame.image.load(path + str(obj) + '.png')
        return surf


class CosherCity(City):
    def __init__(self, name, x, y, tavern, level, wall,
                 skeleton, skeleton_archer, leach,
                 horseman_of_the_apocalypse,
                 necromancer, garrison, hero, hero1, hero2):

        super().__init__()

        # Когда герой заходит в таверну, ему на выбор дается покупка двух героев
        # Они меняются только в случае покупки и уникальны для каждого города
        self.hero1 = hero1
        self.hero2 = hero2

        self.back_ground_surf = pygame.image.load('data\COSHER_CITY_SPRYTE\\background.png').convert()

        self.name = name    # Название города. Показывается в окошках
        self.x = x  # Координата города на карте по оси x
        self.y = y  # Координата города на карте, по оси y
        self.tavern = tavern    # Таверна. В ней можно нанять новых героев.
        self.tavern_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\tavern', '', 1)

        self.level = level    # В зависимости от уровня, можно нанимать разных юнитов
        self.level_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\city_level_', self.level, 1)
        self.wall = wall    # В зависимости от уровня, меняе  уровень защиты
        self.wall_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\wall_level_', self.wall, 1)

        # Здания для постройки юнитов задаются цифрами. Если 0 - такого здания нет. Если
        # 1 - то можно нанимать слабую версию Юнита. Если 2 - то сильную.

        self.skeleton = skeleton    # Самый слабый юнит - скелетон. Доступен с первого уровня.
        if skeleton == 0:
            self.skeleton_surf = None
        else:
            self.skeleton_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\skeleton_level_', self.skeleton, 1)

        self.skeleton_archer = skeleton_archer  # слабый юнит, атакует с дистанции. Доступен с первого уровня
        if self.skeleton_archer > 0:
            self.skeleton_archer_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\skeleton_archer_level_', self.skeleton_archer, 1)
        else:
            self.skeleton_archer_surf = None

        self.leach = leach  # Средний по уровню юнит. Атакует с дистанции. Доступен со второго уровня
        if self.leach > 0:
            self.leach_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\leach_level_', self.leach, 1)
        else:
            self.leach_surf = None

        self.horseman_of_the_apocalypse = horseman_of_the_apocalypse    # Сильный юнит. Доступен со второго уровня
        if self.horseman_of_the_apocalypse > 0:
            self.horseman_of_the_apocalypse_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\horseman_of_the_apocalypse_level_', self.horseman_of_the_apocalypse, 1)
        else:
            self.horseman_of_the_apocalypse_surf = None

        self.necromancer = necromancer  # Юнит поддержки. Способен восстанавливать hp союзникам и поднимать пол армии
        # Доступен с третьего уровня
        if self.necromancer > 0:
            self.necromancer_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\necromancer_level_', self.necromancer, 1)
        else:
            self.necromancer_surf = None

        self.garrison = garrison    # Задается списком из объектов военных юнитов

    def draw_panorama(self):
        screen.blit(self.interface_down_surf,  (0, 562))
        screen.blit(self.back_ground_surf, (0, 0))
        screen.blit(self.level_surf, (630, 110))
        screen.blit(self.wall_surf, (830, 100))
        if self.tavern == 1:
            screen.blit(self.tavern_surf, (220, 300))

        if self.skeleton > 0:
            screen.blit(self.skeleton_surf, (100, 400))

        if self.skeleton_archer > 0:
            screen.blit(self.skeleton_archer_surf, (550, 400))

        if self.leach > 0:
            screen.blit(self.leach_surf, (1000, 400))

        if self.horseman_of_the_apocalypse > 0:
            screen.blit(self.horseman_of_the_apocalypse_surf, (70, 170))

        if self.necromancer > 0:
            screen.blit(self.necromancer_surf, (800, 370))

    def draw_upgrade_city_window(self):  # Заглушка
        pass



city = CosherCity(name='Бакареш', x=2, y=2, tavern=1, level=3, wall=3, skeleton=2,
                  skeleton_archer=1, leach=1, horseman_of_the_apocalypse=2,
                  necromancer=1, garrison=None, hero=None, hero1=None, hero2=None)
run = 1
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if city.active == city.panorama:
                    if 100 < event.pos[0] < 296 and 400 < event.pos[1] < 530:
                        city.active = city.buy_unit
                        city.unit = Skeleton
                    if 70 < event.pos[0] < 125 + 70 and 170 < event.pos[1] < 170 + 192:
                        city.active = city.buy_unit
                        city.unit = HorsemanOfTheApocalypse

                    if 550 < event.pos[0] < 550 + 132 and 400 < event.pos[1] < 400 + 74:
                        city.active = city.buy_unit
                        city.unit = SkeletonArcher

                    if 1000 < event.pos[0] < 1000 + 129 and 400 < event.pos[1] < 400 + 120:
                        city.active = city.buy_unit
                        city.unit = Leach

                    if 70 < event.pos[0] < 70 + 125 and 170 < event.pos[1] < 170 + 193:
                        city.active = city.buy_unit
                        city.unit = HorsemanOfTheApocalypse

                    if 800 < event.pos[0] < 800 + 183 and 370 < event.pos[1] < 370 + 83:
                        city.active = city.buy_unit
                        city.unit = NecroMancer

                    #if 630 < event.pos[0] < 630 + 174 and 110 < event.pos[1] < 110 + 158:
                    #    city.active = city.upgrade_city

                    if 220 < event.pos[0] < 220 + 199 and 300 < event.pos[1] < 300 + 68:
                        city.active = city.buy_hero




        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if city.active == city.buy_unit or city.active == city.buy_hero:    # or city.active == city.upgrade_city
                    city.active = city.panorama
                elif city.active == city.panorama:
                    print("sosat'") # Заглушка

    if city.active == city.panorama:
        city.draw_panorama()

    if city.active == city.buy_unit:
        city.draw_buy_unit_window(city.unit)

    if city.active == city.buy_hero:
        city.draw_buy_hero_window(None, None)   # Заглушка

    if city.active == city.upgrade_city:
        city.draw_upgrade_city_window()

    pygame.display.flip()




