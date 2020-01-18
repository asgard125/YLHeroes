import pygame
from UnitTypes import *
from CosherCity import *
from Heroes import *
import os





# загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Статичная картинка сзади
class BackGround(pygame.sprite.Sprite):
    image = load_image('debug.png')

    def __init__(self):
        super().__init__(all_sprite, bg_sprite)
        self.image = BackGround.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Hero(pygame.sprite.Sprite):
    def __init__(self, name, side, x, y):
        super().__init__(all_sprite, heroes_sprite)

        self.image = load_image(str(name), -1)
        self.rect = self.image.get_rect()

        self.side = str(side)
        self.x = x
        self.y = y
        self.rect.x = self.x * cell_width
        self.rect.y = self.y * cell_width

        self.army = {0, 0, 0, 0, 0, 0, 0}
        self.turns = 27


class City(pygame.sprite.Sprite):
    def __init__(self, name, side, typee, x, y):
        super().__init__(all_sprite, interactive_sprite)

        self.image = load_image(str(name), -1)
        self.rect = self.image.get_rect()

        self.side = str(side)
        self.x = x
        self.y = y
        self.rect.x = self.x * cell_width
        self.rect.y = self.y * cell_width

        self.typee = typee


# Взять координату нажатой позиции
def get_coord(x, y):
    return (x - back_ground.rect.x) // cell_width, (y - back_ground.rect.y) // cell_width


def move(obj, x, x1, y, y1):
    move_p = True  # Разерешние/Запрет движения перемнная

    new_x = obj.x + x
    new_y = obj.y + y

    if new_x < 0 or new_y < 0 or new_x > 32 or new_y > 32:
        move_p = False

    for hero in heroes:
        if hero.x == new_x and hero.y == new_y:
            move_p = False  #Заглушка. Тут должен быть скрипт интерактива двух героев.

    if move_p:
        obj.x += x
        obj.rect.x += x1
        obj.y += y
        obj.rect.y += y1

    move_p = False


def run_map():

    pygame.init()

    # Разрешение экрана
    width = 1200
    height = 1000
    screen = pygame.display.set_mode((width, height))

    # Количество кадров в секунду
    clock = pygame.time.Clock()
    fps = 30

    # Ширина одной клеточки
    cell_width = 60

    # Группы спрайтов
    all_sprite = pygame.sprite.Group()
    bg_sprite = pygame.sprite.Group()
    heroes_sprite = pygame.sprite.Group()
    interactive_sprite = pygame.sprite.Group()

    # Поля
    field = ['0' * 32] * 32   # Поле, по которым двигаются Герои
    interactive = [City('debug_city.png', 'blue', 'cosher', 8, 9)]  # Массив, внутри которого хранятся интерактивные объекты
    heroes = [Hero('debug_hero.png', 'blue', 3, 2), Hero('debug_hero.png', 'blue', 5, 9)]   # Массив, внутри которого хранятся герои

    # Что выбрано сейчас
    active = heroes[0]



    # Переменные
    back_ground = BackGround()


    # Отступы при движении камеры

    # Вкл/выкл переменная
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                # Движение камеры
                if event.key == pygame.K_UP:
                    if back_ground.rect.y <= 500:
                        for sprite in all_sprite:
                            sprite.rect.y += cell_width
                elif event.key == pygame.K_LEFT:
                    if back_ground.rect.x <= 500:
                        for sprite in all_sprite:
                            sprite.rect.x += cell_width
                elif event.key == pygame.K_DOWN:
                    if not back_ground.rect.y <= -1420:
                        for sprite in all_sprite:
                            sprite.rect.y -= cell_width
                elif event.key == pygame.K_RIGHT:
                    if not back_ground.rect.x <= -1420:
                        for sprite in all_sprite:
                            sprite.rect.x -= cell_width

                # Движение героя
                if event.key == pygame.K_w:
                    move(active, 0, 0, -1, -cell_width)
                elif event.key == pygame.K_a:
                    move(active, -1, -cell_width, 0, 0)
                elif event.key == pygame.K_s:
                    move(active, 0, 0, 1, cell_width)
                elif event.key == pygame.K_d:
                    move(active, 1, cell_width, 0, 0)

            # Нажатие на поле
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coords = get_coord(event.pos[0], event.pos[1])
                    for hero in heroes:
                        if hero.x == coords[0] and hero.y == coords[1]:
                            active = hero



        screen.fill((0, 0, 0))
        all_sprite.draw(screen)
        heroes_sprite.draw(screen)
        pygame.display.flip()

        clock.tick(fps)


    pygame.quit()
