import pygame
from UnitTypes import *
from CosherCity import *
from random import choice, randint
from Heroes import *
import os

global gold_player_1, gold_player_2, turn_player_1, turn_player_2, hero_player_1, hero_player_2, status, month, week, day



# загрузка изображений
def load_image(name, direct=None, colorkey=None):
    image = None
    if direct == 'load_level':
        image = pygame.image.load('maps\\' + name)
    elif direct == 'load_object':
        image = pygame.image.load('generatorFiles\\' + name)
    elif direct == 'load_interface':
        image = pygame.image.load('data\\MAP_INTERFACE\\' + name)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

#  Загрузить уровень
def load_level(name):
    maps = os.listdir(path="maps")
    if name + '_background.txt' in maps and name + '_image.png' in maps and name+'_primary.txt' in maps:
        with open('maps/' + name + '_background.txt', 'r') as file:
            passive_objects = [line.strip() for line in file]
        with open('maps/' + name + '_primary.txt', 'r') as file:
            active_objects = [list(i) for i in [line.strip() for line in file]]
        background_image = load_image(name + '_image.png', 'load_level')
        return active_objects, passive_objects, background_image

def draw_map_interface():
    right_int = load_image('right_interface.png', 'load_interface')
    right_int = pygame.transform.scale(right_int, (300, 950))
    if status == turn_player_1:
        flag = load_image('red_flag.png', 'load_interface')
        flag = pygame.transform.scale(flag, (1162 - 941, 278 - 41))
        hero = hero_player_1
    elif status == turn_player_2:
        flag = load_image('blue_flag.png', 'load_interface')
        flag = pygame.transform.scale(flag, (1162 - 941, 278 - 41))
        hero = hero_player_2
    screen.blit(right_int, (900, 0))
    screen.blit(flag, (941, 41))
    draw_down_interface()
    draw_hero_interface(hero)

def draw_hero_interface(hero):
    screen.blit(hero.hero.icon, (970, 1008))
    screen.blit(pygame.font.Font(None, 35).render(hero.hero.name, 1, (255, 255, 255)), (975, 1017))
    screen.blit(pygame.font.Font(None, 35).render(str(hero.hero.attack_bonus), 1, (255, 255, 255)), (925, 1087))
    screen.blit(pygame.font.Font(None, 35).render(str(hero.hero.deffence_bonus), 1, (255, 255, 255)), (945, 1017))


def draw_down_interface():
    global day, month, week
    down_interface = load_image('resorses_interface.png', 'load_interface', 0)
    down_interface = pygame.transform.scale(down_interface, (1200, 50))
    screen.blit(down_interface, (0, 950))
    fonts = pygame.font.Font(None, 20)
    screen.blit(fonts.render('Месяц: {}, Неделя: {} День: {}'.format(str(month), str(week), str(day)), 1, (255, 255, 255)), (930, 965))
    if status == turn_player_1:
        screen.blit(fonts.render(str(gold_player_1), 1, (255, 255, 255)), (815, 965))
    elif status == turn_player_2:
        screen.blit(fonts.render(str(gold_player_2), 1, (255, 255, 255)), (815, 965))

def check_click(x, y, background):
    if background.rect.x + 1920 > x > background.rect.x and background.rect.y + 1920 > y > background.rect.y:
        return (x - background.rect.x ) // 60, (y - background.rect.y) // 60

# ----------------------------------------------------------------------------------------------------------------------Стартовый цикл
def run_map(name):
    pygame.init()


    # Надпись загрузки
    screen.fill(pygame.Color('black'))
    fonts = pygame.font.Font(None, 40)
    screen.blit(fonts.render('Загрузка', 1, (255, 255, 255)), (15, 15))
    pygame.display.flip()

    # Размер клетки
    cell_width = 60

    # Группы спрайтов
    all_sprites = pygame.sprite.Group()
    active_sprites = pygame.sprite.Group()
    bg_sprite = pygame.sprite.Group()
    hero_sprites = pygame.sprite.Group()

    class Background(pygame.sprite.Sprite):
        def __init__(self, image):
            super().__init__(bg_sprite, all_sprites)
            self.image = image
            self.rect = self.image.get_rect()

    class Active(pygame.sprite.Sprite):
        def __init__(self, obj, x, y):
            super().__init__(active_sprites, all_sprites)

            # проверка объекта
            self.image = None
            self.self_type = None
            if obj == '1':
                self.image = load_image('gold.png', 'load_object')
                self.self_type = 'gold'
            elif obj == '2':
                self.image = load_image('necropolis.png', 'load_object')
                self.self_type = 'city'
            self.image = pygame.transform.scale(self.image, (cell_width, cell_width))

            # Холст
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x * cell_width, y * cell_width

            # Координаты
            self.x = x
            self.y = y

    class MapHero(pygame.sprite.Sprite):
        def __init__(self, obj):
            super().__init__(hero_sprites)
            self.image = obj.appearance
            self.image.set_colorkey(self.image.get_at((0, 0)))
            self.rect = self.image.get_rect()

            self.rect.x, self.rect.y = obj.x * cell_width, obj.y * cell_width
            self.hero = obj

        #  Передвижение героя и его интерактив с объектами
        def move_hero(self, x, y):
            global gold_player_1, gold_player_2
            if self.hero.move < self.hero.able_to_move:
                if passive_objects[self.hero.y + y][self.hero.x + x] not in ['2', '3']:

                    self.hero.x += x
                    self.rect.x += cell_width * x
                    self.hero.y += y
                    self.rect.y += cell_width * y

                    if passive_objects[self.hero.y][self.hero.x] == '1':
                        self.hero.move += 100
                    elif passive_objects[self.hero.y][self.hero.x] == '0':
                        self.hero.move += 50

                    if active_objects[self.hero.y][self.hero.x] == '1':
                        active_objects[self.hero.y][self.hero.x] = '*'
                        if status == turn_player_1:
                            gold_player_1 += choice([500, 700])
                        elif status == turn_player_2:
                            gold_player_2 += choice([500, 700])

                        self.hero.expirience += 50
                        if self.hero.expirience >= self.hero.level * self.hero.expirience_border:
                            self.hero.level += 1
                            self.hero.expirience = 0
                            if randint(0, 1):
                                self.hero.attack_bonus += 1
                            else:
                                self.hero.deffence_bonus += 1

                        for sprite in active_sprites:
                            if (sprite.x, sprite.y) == (self.hero.x, self.hero.y) and sprite.self_type == 'gold':
                                sprite.remove(active_sprites)
                                break
                    elif active_objects[self.hero.y][self.hero.x] == '2':
                        print('1')
                        for c in range(len(cities_list)):
                            print('2')
                            if cities_list[c].x == self.hero.x and cities_list[c].y == self.hero.y:
                                print('3')
                                cities_list[c].entered_hero = hero
                                if cities_list[c].city_type == 'cosher':
                                    print('4')
                                    cities_list[c] = run_cosher_city(cities_list[c])
                                    break
                    elif hero_player_1.hero.x == hero_player_2.hero.x and hero_player_1.hero.y == hero_player_2.hero.y:
                        print('start battle here')  # --------------------------------------------------------------------батя и сын снова сцепились по пьяне



    # Настройки карты. Актив, пассив и фон
    active_objects, passive_objects, background_img = load_level(name)

    # Названия городов
    cities_names = ['Бакареш', "Гильотиньина", "Агони", "Центроперколер", "сифка пипивка", "Картофельный", "Дно"]

    # Список в котором находятся города
    cities_list = []

    # Добавление спрайтов на карту
    background = Background(background_img)  # Спрайт фонового изображения
        # Добавление интерактивных объектов в группу спрайтов
    for i in range(len(active_objects)):
        for j in range(len(active_objects[0])):
            if active_objects[i][j] != '*' and active_objects[i][j] != 'q' and active_objects[i][j] != 'w':
                if active_objects[i][j] == '2':
                    cities_list.append(CosherCity(choice(cities_names), j, i, ['', '', '', '', ''], None))
                active = Active(active_objects[i][j], j, i)




    global gold_player_1, gold_player_2, turn_player_1, turn_player_2, hero_player_1, hero_player_2, status, month, week, day

    # Список с существующими героями, чтобы задавать их
    heroes = [Orrin(0, 0), Zuldan(0, 0), Gardon(0, 0)]

    # -------------------------------------------------------------------------------------------------------------------Костыль
    hero_player_1 = None
    hero_player_2 = None
    # -------------------------------------------------------------------------------------------------------------------Костыль

    # Раскидка героев игрокам
    for i in range(len(active_objects)):
        for j in range(len(active_objects[0])):

            # Проверка на то, является ли координата точкой спауна героя 1
            if active_objects[i][j] == 'q':
                hero = choice(heroes)
                hero_player_1 = MapHero(hero)
                hero_player_1.hero.x = j
                hero_player_1.hero.y = i
                hero_player_1.rect.x, hero_player_1.rect.y = hero_player_1.hero.x * cell_width, hero_player_1.hero.y * cell_width
                for i in range(len(heroes)):
                    if heroes[i] == hero_player_1.hero:
                        del heroes[i]
                        break

            # Проверка на то, является ли координата точкой спауна героя 2
            elif active_objects[i][j] == 'w':
                hero = choice(heroes) # Выбирается случайный герой
                hero_player_2 = MapHero(hero)
                hero_player_2.hero.x = j
                hero_player_2.hero.y = i
                hero_player_2.rect.x, hero_player_2.rect.y = hero_player_2.hero.x * cell_width, hero_player_2.hero.y * cell_width
                for i in range(len(heroes)):
                    if heroes[i] == hero_player_2.hero:
                        del heroes[i]
                        break

            # Остановка раскидки героев
            if hero_player_1 != None and hero_player_2 != None:
                break


    # Набор различных статусов
    turn_player_1 = 1   # ход игрока 1
    turn_player_2 = 2   # ход игрока 2

    # золото первого и второго игрока
    gold_player_1 = 0   # Количество золота игрок 1
    gold_player_2 = 0   # Количество золота игрок 2

    # Месяц, неделя, день
    month, week, day = 0, 0, 1


    #Статус в данный момент
    status = turn_player_1



    run = 1
    while run:

        screen.fill(pygame.Color('black'))
        bg_sprite.draw(screen)
        active_sprites.draw(screen)
        hero_sprites.draw(screen)
        pygame.draw.rect(screen, pygame.Color('red'), (hero_player_1.rect.x + 20, hero_player_1.rect.y, 15, 5))
        pygame.draw.rect(screen, pygame.Color('blue'), (hero_player_2.rect.x + 20, hero_player_2.rect.y, 15, 5))
        draw_map_interface()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    for sprite in active_sprites:
                        sprite.rect.y -= cell_width
                    background.rect.y -= cell_width
                    for sprite in hero_sprites:
                        sprite.rect.y -= cell_width

                elif event.key == pygame.K_UP:
                    for sprite in active_sprites:
                        sprite.rect.y += cell_width
                    background.rect.y += cell_width
                    for sprite in hero_sprites:
                        sprite.rect.y += cell_width

                elif event.key == pygame.K_RIGHT:
                    for sprite in active_sprites:
                        sprite.rect.x -= cell_width
                    background.rect.x -= cell_width
                    for sprite in hero_sprites:
                        sprite.rect.x -= cell_width

                elif event.key == pygame.K_LEFT:
                    for sprite in active_sprites:
                        sprite.rect.x += cell_width
                    background.rect.x += cell_width
                    for sprite in hero_sprites:
                        sprite.rect.x += cell_width

                # Движение героев
                move = False
                if event.key == pygame.K_w:
                    move = (0, -1)
                if event.key == pygame.K_d:
                    move = (1, 0)
                if event.key == pygame.K_s:
                    move = (0, 1)
                if event.key == pygame.K_a:
                    move = (-1, 0)

                if move is not False:
                    if status == turn_player_1:
                        hero_player_1.move_hero(move[0], move[1])
                    elif status == turn_player_2:
                        hero_player_2.move_hero(move[0], move[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # следующий ход
                    if 1017 < event.pos[0] < 1117 and 587 < event.pos[1] < 645:
                        if status == turn_player_1:
                            hero_player_1.hero.move = 0
                            status = turn_player_2
                        elif status == turn_player_2:
                            hero_player_2.hero.move = 0
                            status = turn_player_1
                            if day < 7:
                                day += 1
                            else:
                                day = 1
                                for i in range(len(cities_list)):

                                    if cities_list[i].city_type == 'cosher':
                                        cities_list[i].able_skeletons = 14
                                        cities_list[i].able_zombies = 6
                                        cities_list[i].able_leaches = 2

                                    elif cities_list[i].city_type == 'human':
                                        cities_list[i].able_spearman = 12
                                        cities_list[i].able_archer = 10
                                        cities_list[i].able_cavalryman = 4

                                if week != 3:
                                    week += 1
                                else:
                                    week = 0
                                    month += 1
                                    gold_player_1 += 1500
                                    gold_player_2 += 1500
                    else:
                        coords = check_click(event.pos[0], event.pos[1], background)
                        for city in range(len(cities_list)):
                            if cities_list[city].x == coords[0] and cities_list[city].y == coords[1]:
                                if cities_list[city].city_type == 'cosher':
                                    cities_list[city] = run_cosher_city(cities_list[city])
                    print(event.pos)



run_map('test2')