import pygame
import pygame as pg
import random
import os
import math

pg.init()
pygame.font.init()

size = width_, height_ = 1200, 750
win = pygame.display.set_mode(size)

color = (255, 255, 255)


def load_image(name, colorkey=None):
    fullname = os.path.join(f"data/UNIT_IMG_BITTLE", name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]
        self.motion = True
        self.left = 10
        self.top = 10
        self.cell_size = 50

        self.img = 'defense_button.png'
        self.kl_img = load_image(self.img, -1).convert()
        self.kl_img = pygame.transform.rotate(self.kl_img, 0)
        self.kl_img = pygame.transform.scale(self.kl_img, (50, 50))
        self.kl = pygame.sprite.Sprite()
        self.kl.image = self.kl_img
        self.kl.rect = self.kl.image.get_rect()
        self.kl.rect.x = 30
        self.kl.rect.y = 600
        self.mob_gr = pygame.sprite.Group()
        self.mob_gr.add(self.kl)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        self.button_defense()
        for n in range(self.height + 1):
            for i in range(self.width + 1):
                pygame.draw.line(win, color, (self.left + i * self.cell_size, self.top + n * self.cell_size),
                                 (self.left + self.width * self.cell_size, self.top + n * self.cell_size))
                pygame.draw.line(win, color, (self.left + i * self.cell_size, self.top + n * self.cell_size),
                                 (self.left + i * self.cell_size, self.top + self.height * self.cell_size))

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y
        return False

    def button_defense(self, event=False):
        self.mob_gr.draw(win)
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 30 <= event.pos[0] < 80 and 600 <= event.pos[1] < 650:
                    print(1)
                    return True


class Mob(pygame.sprite.Sprite):
    def __init__(self, starting_position, coin=10):
        super().__init__()
        self.font = pygame.font.SysFont(None, 30)
        self.coin = coin
        self.starting_position = starting_position
        self.place = starting_position
        self.destination = self.place
        self.left = 10
        self.top = 10
        self.cell_size = 5
        self.img = 'Skeleton.gif'
        self.kl_img = load_image(self.img, -1).convert()
        self.kl_img = pygame.transform.rotate(self.kl_img, 0)
        self.kl_img = pygame.transform.scale(self.kl_img, (50, 50))
        self.speed = 20
        self.speed_i = 20
        self.hp = 10
        self.hp_now = self.hp
        self.attaka = 2
        self.overall_hp = self.hp * self.coin
        self.long_range_attack = False

    def speed_(self):
        self.speed = self.speed_i

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        if self.speed:
            self.kl = pygame.sprite.Sprite()
            self.kl.image = self.kl_img
            self.kl.rect = self.kl.image.get_rect()

            if self.destination[0] > self.place[0]:
                self.place[0] += 1
                self.speed -= 1
            elif self.destination[0] < self.place[0]:
                self.place[0] -= 1
                self.speed -= 1
            elif self.destination[1] > self.place[1]:
                self.place[1] += 1
                self.speed -= 1
            elif self.destination[1] < self.place[1]:
                self.place[1] -= 1
                self.speed -= 1

            self.kl.rect.x = self.left + self.place[0] * self.cell_size
            self.kl.rect.y = self.top + self.place[1] * self.cell_size
            self.mob_gr = pygame.sprite.Group()
            self.mob_gr.add(self.kl)
            pygame.time.wait(15)
        self.mob_gr.draw(win)
        text_coin = self.font.render(f'{self.coin}', 1, (180, 0, 0))
        win.blit(text_coin, (self.kl.rect.x + 20, self.kl.rect.y + 40))

        if self.speed == 0:
            self.destination = self.place
            return True
        return False

    def place_render(self, xy):
        if xy != None:
            self.destination = xy
        if self.destination[0] == self.place[0] and self.destination[1] == self.place[1]:
            return True
        if self.speed == 0:
            return True
        return False
            # print(self.destination)

    def xpeed_replenishment(self):
        self.speed = self.speed_i

    def viability(self, damage):
        if self.overall_hp < damage:
            self.coin = 0
            return True
        else:
            self.overall_hp -= damage
            self.coin = math.ceil(self.overall_hp / self.hp)
            self.hp_now = self.overall_hp % self.hp
            return False

    def brunt(self):
        return self.coin * self.attaka


class Connicks(Mob):
    def __init__(self, starting_position, coin):
        super().__init__(starting_position, coin)
        self.destination = self.place
        self.starting_position = starting_position
        self.img = 'Cavalryman.gif'
        self.kl_img = load_image(self.img, -1).convert()
        self.kl_img = pygame.transform.rotate(self.kl_img, 0)
        self.kl_img = pygame.transform.scale(self.kl_img, (65, 65))
        self.speed = 12
        self.speed_i = 12
        self.hp = 20
        self.hp_now = self.hp
        self.attaka = 15
        self.overall_hp = self.hp * self.coin
        self.long_range_attack = False


class Archers(Mob):
    def __init__(self, starting_position, coin):
        super().__init__(starting_position, coin)
        self.starting_position = starting_position
        self.destination = self.place
        self.img = 'Archer.gif'
        self.kl_img = load_image(self.img, -1).convert()
        self.kl_img = pygame.transform.rotate(self.kl_img, 0)
        self.kl_img = pygame.transform.scale(self.kl_img, (50, 50))
        self.speed = 5
        self.speed_i = 5
        self.hp = 15
        self.hp_now = self.hp
        self.attaka = 7
        self.overall_hp = self.hp * self.coin
        self.long_range_attack = True


class Skeletons(Mob):
    def __init__(self, starting_position, coin):
        super().__init__(starting_position, coin)
        self.destination = self.place
        self.starting_position = starting_position
        self.img = 'Skeleton.gif'
        self.kl_img = load_image(self.img, -1).convert()
        self.kl_img = pygame.transform.rotate(self.kl_img, 0)
        self.kl_img = pygame.transform.scale(self.kl_img, (60, 60))
        self.speed = 4
        self.speed_i = 4
        self.hp = 40
        self.hp_now = self.hp
        self.attaka = 1
        self.overall_hp = self.hp * self.coin
        self.long_range_attack = False


class Spears(Mob):
    def __init__(self, starting_position, coin):
        super().__init__(starting_position, coin)
        self.destination = self.place
        self.starting_position = starting_position
        self.img = 'Spearman.gif'
        self.kl_img = load_image(self.img, -1).convert()
        self.kl_img = pygame.transform.rotate(self.kl_img, 0)
        self.kl_img = pygame.transform.scale(self.kl_img, (50, 50))
        self.speed = 6
        self.speed_i = 6
        self.hp = 15
        self.hp_now = self.hp
        self.attaka = 4
        self.overall_hp = self.hp * self.coin
        self.long_range_attack = False


class Zombie(Mob):
    def __init__(self, starting_position, coin):
        super().__init__(starting_position, coin)
        self.destination = self.place
        self.starting_position = starting_position
        self.img = 'Zombi.gif'
        self.kl_img = load_image(self.img, -1).convert()
        self.kl_img = pygame.transform.rotate(self.kl_img, 0)
        self.kl_img = pygame.transform.scale(self.kl_img, (50, 50))
        self.speed = 4
        self.speed_i = 4
        self.hp = 70
        self.hp_now = self.hp
        self.attaka = 3
        self.overall_hp = self.hp * self.coin
        self.long_range_attack = False


class Lychee(Mob):
    def __init__(self, starting_position, coin):
        super().__init__(starting_position, coin)
        self.destination = self.place
        self.starting_position = starting_position
        self.img = 'Leach.gif'
        self.kl_img = load_image(self.img, -1).convert()
        self.kl_img = pygame.transform.rotate(self.kl_img, 0)
        self.kl_img = pygame.transform.scale(self.kl_img, (60, 60))
        self.speed = 5
        self.speed_i = 5
        self.hp = 30
        self.hp_now = self.hp
        self.attaka = 4
        self.overall_hp = self.hp * self.coin
        self.long_range_attack = True


class Motion:
    def __init__(self, list_mobs, flag_good=True):
        self.flag_good = flag_good
        self.motin = 0
        self.run = True
        self.kindn_ = list_mobs
        self.kindness = []
        self.y_ = 0
        if self.flag_good:
            self.x_ = 0
        else:
            self.x_ = 14
        self.mob_pos = []

        for i in range(len(self.kindn_)):
            self.star_pos = [self.x_, self.y_]
            if self.kindn_[i][0] == "Скелеты":
                self.kindness.append(Skeletons(self.star_pos, self.kindn_[i][1]))
            elif self.kindn_[i][0] == "Копейщики":
                self.kindness.append(Spears(self.star_pos, self.kindn_[i][1]))
            elif self.kindn_[i][0] == "Зомби":
                self.kindness.append(Zombie(self.star_pos, self.kindn_[i][1]))
            elif self.kindn_[i][0] == "Конники":
                self.kindness.append(Connicks(self.star_pos, self.kindn_[i][1]))
            elif self.kindn_[i][0] == "Личи":
                self.kindness.append(Lychee(self.star_pos, self.kindn_[i][1]))
            elif self.kindn_[i][0] == "Лучники":
                self.kindness.append(Archers(self.star_pos, self.kindn_[i][1]))
            self.y_ += 2
        self.pos()

        self.img = 'field4.jpg'
        self.kl_img = load_image(self.img, -1).convert()
        self.kl_img = pygame.transform.rotate(self.kl_img, 0)
        self.kl_img = pygame.transform.scale(self.kl_img, (1200, 750))
        self.field = pygame.sprite.Sprite()
        self.field.image = self.kl_img
        self.field.rect = self.field.image.get_rect()
        self.field.rect.x = 0
        self.field.rect.y = 0
        self.field_gr = pygame.sprite.Group()
        self.field_gr.add(self.field)

        self.img = 'final_battle.png'
        self.final_img = load_image(self.img, -1).convert()
        self.final_img = pygame.transform.rotate(self.final_img, 0)
        self.final_img = pygame.transform.scale(self.final_img, (700, 750))
        self.final = pygame.sprite.Sprite()
        self.final.image = self.final_img
        self.final.rect = self.field.image.get_rect()
        self.final.rect.x = 200
        self.final.rect.y = 0
        self.final_gr = pygame.sprite.Group()
        self.final_gr.add(self.final)
        self.font = pygame.font.SysFont(None, 100)

        self.run = True

    def render_field(self):
        self.field_gr.draw(win)

    def pos(self):
        self.mob_pos = []
        for i in self.kindness:
            self.mob_pos.append(i.starting_position)

    def move(self, event, board, mob, m):
        self.pos()
        if board.button_defense(event):
            self.motin += 1
            return 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if board.get_cell(event.pos):
                prov = [board.get_cell(event.pos)[0], board.get_cell(event.pos)[1]]
                if event.button == 1 and not(self.mob_pos.count(prov)) and not(m.mob_pos.count(prov)):  # !!!
                    W = False
                    while not W:
                        win.fill((0, 0, 0))
                        self.render_field()
                        board.render()
                        self.render()
                        m.render()
                        pygame.display.flip()
                        W = mob.place_render(board.get_cell(event.pos))
                        if W:
                            self.motin += 1
                            self.pos()
                            return 1

                if event.button == 1 and m.mob_pos.count(prov):
                    W = False
                    n = 0
                    for i in range(len(m.mob_pos)):
                        if m.mob_pos[i] == prov:
                            n = i
                    pos = [board.get_cell(event.pos)[0], board.get_cell(event.pos)[1]]
                    if mob.place[1] > m.kindness[n].place[1]:
                        pos[1] += 1
                    elif mob.place[1] < m.kindness[n].place[1]:
                        pos[1] -= 1
                    elif mob.place[0] > m.kindness[n].place[0]:
                        pos[0] += 1
                    elif mob.place[0] < m.kindness[n].place[0]:
                        pos[0] -= 1
                    if mob.long_range_attack:
                        flag_kil = False
                        flag_kil = m.kindness[n].viability(mob.brunt())
                        if flag_kil:
                            del m.kindness[n]
                            if len(m.kindness) == 0:
                                self.run = False
                            m.pos()
                        self.motin += 1
                        self.pos()
                        return 2
                    else:
                        while not W:
                            self.render_field()
                            self.render()
                            m.render()
                            board.render()
                            pygame.display.flip()
                            W = mob.place_render(pos)
                            if W:
                                flag_kil = False
                                if pos == mob.place:
                                    flag_kil = m.kindness[n].viability(mob.brunt())
                                if flag_kil:
                                    del m.kindness[n]
                                    if len(m.kindness) == 0:
                                        self.run = False
                                    m.pos()
                                self.motin += 1
                                self.pos()
                                return 2

    def move_ol(self, event, board, m):
        if self.motin == len(self.kindness):
            self.motin = 0
            for i in self.kindness:
                i.speed_()
            return True
        self.move(event, board, self.kindness[self.motin], m)
        return False

    def render(self):
        for i in self.kindness:
            i.render()

    def set_view(self, left, top, cell_size):
        for i in self.kindness:
            i.set_view(left, top, cell_size)

    def declaration_of_victory(self, event):
        self.final_gr.draw(win)
        text_coin = self.font.render(f'Победа', 1, (180, 0, 0))
        win.blit(text_coin, (self.final.rect.x + 200, self.final.rect.y + 290))
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 775 <= event.pos[0] < 872 and 670 <= event.pos[1] < 722:
                    return False
        return True

    def running_broadcast(self):
        return self.run


class Main:
    def __init__(self, W1, Z1):
        pygame.mixer.music.load(f'data/MUSIC/introduction_battle.mp3')
        pygame.mixer.music.play()
        m1 = Motion(W1, True)
        m2 = Motion(Z1, False)
        board = Board(15, 10)
        board.set_view(100, 130, 60)
        m1.set_view(100, 130, 60)
        m2.set_view(100, 130, 60)
        self.running = True
        self.running2 = True
        mot = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                board.button_defense(event)
                if mot:
                    w = m1.move_ol(event, board, m2)
                    if w:
                        mot = False
                else:
                    w = m2.move_ol(event, board, m1)
                    if w:
                        mot = True
            self.running = m1.running_broadcast()
            m1.render_field()
            m1.render()
            m2.render()
            board.render()
            pygame.display.flip()

        while self.running2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running2 = False
                self.running2 = m1.declaration_of_victory(event)
            pygame.display.flip()


m = Main([["Скелеты", 17], ["Конники", 35], ["Лучники", 35], ["Личи", 35]], [["Скелеты", 17], ["Личи", 100]])
