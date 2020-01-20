from UnitTypes import *


def load_sprite(path, check=0):
    if check:
        surf = pygame.image.load(path + '.png')
        surf.set_colorkey(surf.get_at((0, 0)))
    else:
        surf = pygame.image.load(path + '.png')
    return surf


class Hero:
    def __init__(self, x, y, name, icon, city_icon, mini_icon, appearance, attack_bonus, deffence_bonus, army, able_to_move):
        self.x = x
        self.y = y

        # Набор иконок. 1 - на карте, 2 - в городе, 3 - справа, в менюшке быстрого доступа
        self.icon = icon
        self.city_icon = city_icon
        self.mini_icon = mini_icon

        # Имя и внешность на карте
        self.name = name
        self.appearance = appearance

        # Бонусы, которые получает армия
        self.attack_bonus = attack_bonus
        self.deffence_bonus = deffence_bonus

        # Сама армия
        self.army = army

        # Возможность двигаться
        self.able_to_move = able_to_move
        self.move = 0

        # Увеличение уровня
        self.level = 1
        self.expirience_border = 700
        self.expirience = 0


class Orrin(Hero):
    def __init__(self, x, y):
        super().__init__(x, y, 'Оррин', load_sprite('data\HEROES_ICONS\Hero_icon_orrin'),
                         load_sprite('data\HEROES_ICONS\Hero_icon_orrin_mini'),
                         load_sprite('data\HEROES_ICONS\Hero_icon_orrin_city'),
                         load_sprite('data\HEROES_APPEARANCE\Knight_icon', 1),
                         1, 4, [SpearMan(10), Archer(6), '', '', ''], 800)


class Zuldan(Hero):
    def __init__(self, x, y):
        super().__init__(x, y, 'Зулдан', load_sprite('data\HEROES_ICONS\Hero_icon_zuldan', 0),
                         load_sprite('data\HEROES_ICONS\Hero_icon_zuldan_city', 0),
                         load_sprite('data\HEROES_ICONS\Hero_icon_zuldan_mini', 0),
                         load_sprite('data\HEROES_APPEARANCE\Skeleton_icon', 1),
                         2, 1, [Skeleton(12), '', '', '', ''], 1000)

class Gardon(Hero):
    def __init__(self, x, y):
        super().__init__(x, y, 'Гардъон', load_sprite('data\HEROES_ICONS\Hero_icon_gardon'),
              load_sprite('data\HEROES_ICONS\Hero_icon_gardon_mini'),
              load_sprite('data\HEROES_ICONS\Hero_icon_gardon_city'),
              load_sprite('data\HEROES_APPEARANCE\Knight_icon', 1),
              1, 4, [SpearMan(18), Archer(4), '', '', ''], 890)




