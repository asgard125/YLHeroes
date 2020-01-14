import pygame
from UnitTypes import *


pygame.init()

width = 1200
height = 1000
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Город нежити')


# хранит параметры, для отрисовки окон и окошек
class City:
    def __init__(self, city_type, garrison, hero1, hero2):
        # Разные статусы, благодаря которым происходит отрисовка
        self.panorama = 0
        self.buy_unit = 1
        self.buy_hero = 2
        self.upgrade_city = 3
        self.unit = None    # Заглушка
        self.able = None

        # Статус в данный конкертный момент отрисовки
        self.active = self.panorama

        # Разные Surface для работы интерфейса
        self.interface_down_surf = self.load_sprite("data\ALL_CITIES_SPRYTES\interface_down", '', 0)
        self.buy_unit_surf = self.load_sprite('data\ALL_CITIES_SPRYTES\interface_buy_unit', '', 0)
        self.buy_unit_bg_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\Cosher_buy_unit_bg', '', 0)
        self.buy_hero_surf = self.load_sprite('data\ALL_CITIES_SPRYTES\\interface_buy_hero', '', 0)

        # 2 героя, доступных для покупки в таверне
        self.hero1 = hero1
        self.hero2 = hero2

        # Гарнизон города
        self.garrison = garrison


        # Пара костылей
        self.count = 0  # Переменная, которая изменяется, когда выбираешь, сколько юнитов купить

        # Возможность купить Юнит. Общее для всех.
        if city_type == 'cosher':
            self.able_skeletons = 14
            self.able_zombies = 6
            self.able_leaches = 2
        elif city_type == 'human':
            self.able_spearman = 12
            self.able_archer = 10
            self.able_cavalryman = 4


    # Отрисовка разных видов интерфейса
    # Отрисовка найма юнитов
    def draw_buy_unit_window(self, unit, able, back_ground):
        screen.blit(self.buy_unit_surf, (164, 143))
        screen.blit(back_ground, (511, 262))
        unit_surf = pygame.transform.scale(unit.image, (140, 200))
        screen.blit(unit_surf, (520, 280))
        self.draw_buy_unit_text(unit.name, unit.price, self.count, able)

    def draw_buy_unit_text(self, name, price, c, able_to_buy):
        fonts = pygame.font.Font(None, 40)
        screen.blit(fonts.render('Нанять: ' + name, 3, (255, 255, 255)), (460, 182))
        screen.blit(fonts.render(str(price), 2, (255, 255, 255)), (350, 650))
        screen.blit(fonts.render(str(able_to_buy - c), 1, (255, 255, 255)), (501, 585))
        screen.blit(fonts.render(str(c), 1, (255, 255, 255)), (646, 590))
        screen.blit(fonts.render(str(price * c), 1, (255, 255, 255)), (810, 649))

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
                 skeleton, zombie, leach,
                 horseman_of_the_apocalypse,
                 necromancer, garrison, hero, hero1, hero2):

        super().__init__('cosher', garrison, hero1, hero2)

        # Количество юнитов доступных для покупки сейчас


        self.back_ground_surf = pygame.image.load('data\COSHER_CITY_SPRYTE\\background.png').convert()

        self.name = name
        self.x = x
        self.y = y
        self.tavern = tavern
        self.tavern_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\tavern', '', 1)

        self.level = level    # В зависимости от уровня, можно нанимать разных юнитов
        self.level_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\city_level_', self.level, 1)
        self.wall = wall    # В зависимости от уровня, меняе  уровень защиты
        self.wall_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\wall_level_', self.wall, 1)

        self.skeleton = skeleton
        if skeleton == 0:
            self.skeleton_surf = None
        else:
            self.skeleton_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\skeleton_level_', self.skeleton, 1)

        self.zombie = zombie
        if self.zombie > 0:
            self.zombie_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\skeleton_archer_level_', self.zombie, 1)
        else:
            self.zombie_surf = None

        self.leach = leach
        if self.leach > 0:
            self.leach_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\leach_level_', self.leach, 1)
        else:
            self.leach_surf = None

        self.horseman_of_the_apocalypse = horseman_of_the_apocalypse
        if self.horseman_of_the_apocalypse > 0:
            self.horseman_of_the_apocalypse_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\horseman_of_the_apocalypse_level_', self.horseman_of_the_apocalypse, 1)
        else:
            self.horseman_of_the_apocalypse_surf = None

        self.necromancer = necromancer
        if self.necromancer > 0:
            self.necromancer_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\\necromancer_level_', self.necromancer, 1)
        else:
            self.necromancer_surf = None


    def draw_panorama(self):
        screen.blit(self.interface_down_surf,  (0, 562))
        screen.blit(self.back_ground_surf, (0, 0))
        screen.blit(self.level_surf, (630, 110))
        screen.blit(self.wall_surf, (830, 100))
        if self.tavern == 1:
            screen.blit(self.tavern_surf, (220, 300))

        if self.skeleton > 0:
            screen.blit(self.skeleton_surf, (100, 400))

        if self.zombie > 0:
            screen.blit(self.zombie_surf, (550, 400))

        if self.leach > 0:
            screen.blit(self.leach_surf, (1000, 400))

        if self.horseman_of_the_apocalypse > 0:
            screen.blit(self.horseman_of_the_apocalypse_surf, (70, 170))

        if self.necromancer > 0:
            screen.blit(self.necromancer_surf, (800, 370))

    def draw_upgrade_city_window(self):      # <----------------------------------------------------------------------------- Заглушка
        pass



city = CosherCity(name='Бакареш', x=2, y=2, tavern=1, level=1, wall=1, skeleton=1,
                  zombie=1, leach=1, horseman_of_the_apocalypse=1,
                  necromancer=1, garrison=['', '', '', '', '', '', ''], hero=None, hero1=None, hero2=None)
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
                        city.unit = Skeleton(0)
                        city.able = city.able_skeletons

                    if 550 < event.pos[0] < 550 + 132 and 400 < event.pos[1] < 400 + 74:
                        city.active = city.buy_unit
                        city.unit = Zombie(0)
                        city.able = city.able_zombies

                    if 1000 < event.pos[0] < 1000 + 129 and 400 < event.pos[1] < 400 + 120:
                        city.active = city.buy_unit
                        city.unit = Leach(0)
                        city.able = city.able_leaches

                    # < -------------------------------------------------------------------------------------------------Заглушки

                    # if 70 < event.pos[0] < 70 + 125 and 170 < event.pos[1] < 170 + 193:
                    #     city.active = city.buy_unit
                    #     city.unit = HorsemanOfTheApocalypse

                    # if 800 < event.pos[0] < 800 + 183 and 370 < event.pos[1] < 370 + 83:
                    #     city.active = city.buy_unit
                    #     city.unit = NecroMancer

                    #if 630 < event.pos[0] < 630 + 174 and 110 < event.pos[1] < 110 + 158:
                    #    city.active = city.upgrade_city

                    # if 220 < event.pos[0] < 220 + 199 and 300 < event.pos[1] < 300 + 68:
                    #     city.active = city.buy_hero

                if city.active == city.buy_unit:
                    print(event.pos)    #<-------------------------------------------------------------------------------Костыль
                    if 684 < event.pos[0] < 801 and 705 < event.pos[1] < 764:
                        city.count = 0
                        city.unit = None
                        city.active = city.panorama
                    if 476 < event.pos[0] < 511 and 645 < event.pos[1] < 676:
                        if city.count != 0:
                            city.count -= 1
                    if 691 < event.pos[0] < 729 and 648 < event.pos[1] < 678:
                        if city.count != city.able:
                            city.count += 1


                if city.active == city.buy_hero:
                    if 802 < event.pos[0] < 919 and 815 < event.pos[1] < 876:
                        city.active = city.panorama


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if city.active == city.buy_unit or city.active == city.buy_hero:    # or city.active == city.upgrade_city
                    city.active = city.panorama
                elif city.active == city.panorama:
                    print("sosat'")  # <---------------------------------------------------------------------------------Заглушка

    if city.active == city.panorama:
        city.draw_panorama()

    if city.active == city.buy_unit:

        city.draw_buy_unit_window(city.unit, city.able, city.buy_unit_bg_surf)


    if city.active == city.buy_hero:
        city.draw_buy_hero_window(None, None)   # <----------------------------------------------------------------------Заглушка

    if city.active == city.upgrade_city:
        city.draw_upgrade_city_window()

    pygame.display.flip()




