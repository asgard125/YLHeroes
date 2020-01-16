import pygame
from UnitTypes import *
from Heroes import *


pygame.init()

width = 1200
height = 1000
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Город нежити')


# хранит параметры, для отрисовки окон и окошек
class City:
    def __init__(self, name, city_type, garrison, hero1, hero2, hero_in_city, entered_hero):
        # Разные статусы, благодаря которым происходит отрисовка
        self.panorama = 0
        self.buy_unit = 1
        self.buy_hero = 2
        self.upgrade_city = 3
        self.unit = None    # Заглушка

        self.name = name

        # Статус в данный конкертный момент отрисовки
        self.active = self.panorama

        # Разные Surface для работы интерфейса
        self.buy_hero_surf = self.load_sprite('data\ALL_CITIES_SPRYTES\\interface_buy_hero', '', 0)
        self.interface_down_surf = self.load_sprite("data\ALL_CITIES_SPRYTES\interface_down", '', 0)
        self.buy_unit_surf = self.load_sprite('data\ALL_CITIES_SPRYTES\interface_buy_unit', '', 0)
        if city_type == 'cosher':
            self.buy_unit_bg_surf = self.load_sprite('data\COSHER_CITY_SPRYTE\Cosher_buy_unit_bg', '', 0)
            self.city_icon = self.load_sprite('data\\COSHER_CITY_SPRYTE\\cosher_icon', '', 0)

        # 2 героя, доступных для покупки в таверне
        # self.hero1 = hero1
        # self.hero2 = hero2

        # Гарнизон города
        #self.hero_in_garrison = hero_in_city
        self.garrison = garrison

        # герой который вошел в город
        self.entered_hero = entered_hero

        # Пара костылей
        self.count = 0  # Переменная, которая изменяется, когда выбираешь, сколько юнитов купить
        self.able = None

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

    def draw_unit_icon_down_interface(self):
        x = 22, 110
        y = 586, 714
        screen.blit(pygame.transform.scale(self.city_icon, (x[1] - x[0], y[1] - y[0])), (x[0], y[0]))
        fonts = pygame.font.Font(None, 40)
        screen.blit(fonts.render(str(self.name), 1, (255, 255, 255)), (125, 592))
        for i in range(len(self.garrison)):
            if i == 0:
                x = 457, 547
                y = 586, 713
            if i == 1:
                x = 550, 638
                y = 586, 714
            if i == 2:
                x = 645, 730
            if i == 3:
                x = 735, 824
            if i == 4:
                x = 829, 914

            if self.garrison[i] != '':
                if self.garrison[i].count == 0:
                    self.garrison[i] = ''
                    break
                s = self.garrison[i].image
                bg = self.buy_unit_bg_surf
                s = pygame.transform.scale(s, (x[1] - x[0], y[1] - y[0]))
                bg = pygame.transform.scale(bg, (x[1] - x[0], y[1] - y[0]))
                screen.blit(bg, (x[0], y[0]))
                screen.blit(s, (x[0], y[0]))
                fonts = pygame.font.Font(None, 40)
                screen.blit(fonts.render(str(self.garrison[i].count), 1, (255, 255, 255)), (x[0] + 30, y[0] + 101))

        if self.entered_hero is not None:
            x = 362, 449
            y = 775, 904
            screen.blit(pygame.transform.scale(self.entered_hero.city_icon, (x[1] - x[0], y[1] - y[0])), (x[0], y[0]))
            for i in range(len(self.entered_hero.army)):
                if i == 0:
                    x = 457, 545
                    y = 775, 904
                if i == 1:
                    x = 549, 638
                    y = 775, 902
                if i == 2:
                    x = 644, 730
                    y = 775, 904
                if i == 3:
                    x = 736, 824
                if i == 4:
                    x = 829, 916

                if self.entered_hero.army[i] != '':
                    s = self.entered_hero.army[i].image
                    bg = self.buy_unit_bg_surf
                    s = pygame.transform.scale(s, (x[1] - x[0], y[1] - y[0]))
                    bg = pygame.transform.scale(bg, (x[1] - x[0], y[1] - y[0]))
                    screen.blit(bg, (x[0], y[0]))
                    screen.blit(s, (x[0], y[0]))
                    fonts = pygame.font.Font(None, 40)
                    screen.blit(fonts.render(str(self.entered_hero.army[i].count), 1, (255, 255, 255)), (x[0] + 30, y[0] + 101))

    # def draw_buy_hero_window(self, hero1, hero2):
    #     screen.blit(self.buy_hero_surf, (247, 48))

    def load_sprite(self, path, obj, check):
        if check:
            surf = pygame.image.load(path + str(obj) + '.png')
            surf.set_colorkey(surf.get_at((0, 0)))
        else:
            surf = pygame.image.load(path + str(obj) + '.png')
        return surf

    def check_click_garrison(self, x, y):
        if 586 < y < 713:
            if 457 < x < 547:
                return 0
            if 550 < x < 639:
                return 1
            if 642 < x < 728:
                return 2
            if 735 < x < 823:
                return 3
            if 829 < x < 914:
                return 4
        return 5

    def check_unit(self, unit):
        if unit.name == 'Скелеты':
            self.able_skeletons -= self.count
        elif unit.name == 'Зомби':
            self.able_zombies -= self.count
        elif unit.name == 'Личи':
            self.able_leaches -= self.count
        elif unit.name == 'Лучники':
            self.able_archer -= self.count
        elif unit.name == 'Копейщики':
            self.able_spearman -= self.count
        elif unit.name == 'Конники':
            self.able_cavalryman -= self.count


class CosherCity(City):
    def __init__(self, name, x, y, tavern, level, wall,
                 skeleton, zombie, leach,
                 horseman_of_the_apocalypse,
                 necromancer, garrison, hero_in_garrison, entered_hero, hero1, hero2):

        super().__init__(name, 'cosher', garrison, hero1, hero2, hero_in_garrison, entered_hero)

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
        self.draw_unit_icon_down_interface()
        screen.blit(self.back_ground_surf, (0, 0))
        screen.blit(self.level_surf, (630, 200))
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






city = CosherCity(name='Бакареш', x=2, y=2, tavern=0, level=3, wall=3, skeleton=1,
                  zombie=1, leach=1, horseman_of_the_apocalypse=0,
                  necromancer=0, garrison=['', '', '', '', '', '', ''], hero_in_garrison=None, entered_hero = Zuldan(2, 2), hero1=None, hero2=None)
run = 1

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if type(city.active) == tuple:
                    if city.active[0] in city.garrison:
                        check = city.check_click_garrison(event.pos[0], event.pos[1])
                        if check < 5:
                            print(city.active)
                            if check == city.active[1]:
                                pass
                            elif city.garrison[check] == '':
                                city.garrison[check] = city.active[0]
                                city.garrison[city.active[1]] = ''
                                city.active = city.panorama
                            elif city.garrison[check].name == city.active[0].name:
                                city.garrison[check].count += city.active[0].count
                                city.garrison[city.active[1]] = ''
                                city.active = city.panorama
                            else:
                                city.garrison[check], city.garrison[city.active[1]] = city.garrison[city.active[1]], city.garrison[check]
                                city.active = city.panorama
                        print(check, 's',
                              city.garrison[check], 's',
                              city.garrison[0], 's',
                              city.active)
                        break

                if city.active == city.panorama:
                    # print(event.pos[0])
                    if 100 < event.pos[0] < 296 and 400 < event.pos[1] < 530:
                        city.active = city.buy_unit
                        city.unit = Skeleton(city.able_skeletons)
                        city.able = city.able_skeletons

                    if 550 < event.pos[0] < 550 + 132 and 400 < event.pos[1] < 400 + 74:
                        city.active = city.buy_unit
                        city.unit = Zombie(city.able_zombies)
                        city.able = city.able_zombies

                    if 1000 < event.pos[0] < 1000 + 129 and 400 < event.pos[1] < 400 + 120:
                        city.active = city.buy_unit
                        city.unit = Leach(city.able_leaches)
                        city.able = city.able_leaches

                    check = city.check_click_garrison(event.pos[0], event.pos[1])
                    if check < 5:
                        if city.garrison[check] != '':
                            city.active = (city.garrison[check], check)

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
                    if 399 < event.pos[0] < 514 and 706 < event.pos[1] < 758:
                        if city.count > 0:
                            for i in range(len(city.garrison)):
                                if city.garrison[i] != '':
                                    if city.garrison[i].name == city.unit.name:
                                        city.garrison[i].count += city.count
                                        city.check_unit(city.garrison[i])
                                        city.count = 0
                                        city.active = city.panorama
                                        break
                                elif city.garrison[i] == '':
                                    city.garrison[i] = city.unit
                                    city.check_unit(city.garrison[i])
                                    city.garrison[i].count = city.count
                                    city.count = 0
                                    city.active = city.panorama
                                    break



                # Закрытие окна магазина
                if city.active == city.buy_hero:
                    if 802 < event.pos[0] < 919 and 815 < event.pos[1] < 876:
                        city.active = city.panorama

        # Закрытие окон и самого города
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if city.active == city.buy_unit or city.active == city.buy_hero:    # or city.active == city.upgrade_city
                    city.active = city.panorama
                elif city.active == city.panorama:
                    print("Нот энд'")  # <---------------------------------------------------------------------------------Заглушка

    if city.active == city.panorama:
        city.draw_panorama()

    if city.active == city.buy_unit:
        city.draw_buy_unit_window(city.unit, city.able, city.buy_unit_bg_surf)

    pygame.display.flip()



