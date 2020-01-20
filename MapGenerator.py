import pygame as pg
import os
from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageDraw


def load_image(name, colorkey=None):  # загрузка изображения
    fullname = os.path.join('generatorFiles', name)
    image = pg.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class PgButton:
    def __init__(self, xy, wh, image):
        self.xy = xy
        self.wh = wh
        self.image = pg.transform.scale(image, wh)

    def draw_button(self, surface):
        surface.blit(self.image, (self.xy[0], self.xy[1]))

    def check_hit(self, pos):
        return self.xy[0] <= pos[0] <= self.xy[0] + self.wh[0] and self.xy[1] <= pos[1] <= self.xy[1] + self.wh[1]


class GameObject(pg.sprite.Sprite):  # класс спрайтов
    def __init__(self, cords, pos, name=None, image=None, obj_type=None, placeable=None, txt_char=None):
        super().__init__()
        self.pos = pos
        self.image = pg.transform.scale(load_image(image), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = cords[0]
        self.rect.y = cords[1]
        self.txt_char = txt_char
        self.obj_type = obj_type
        self.name = name
        self.placeable = placeable
        self.img_name = image


class Board:
    def __init__(self, width, height):
        # все доски и текстовое представление
        self.primary_board = [['*'] * width for _ in range(height)]
        self.background_board = [[GameObject((
            i * 30 + (1280 - 30 * 16) // 2, j * 30 + 10),
            (j, i),
            **{'name': 'Grass', 'image': 'grass.png', "obj_type": 'background', 'placeable': True, 'txt_char': '0'}) for
            i in range(width)] for j in range(height)]
        self.txt_primary_map = [['*'] * width for _ in range(height)]
        self.txt_background_map = [['0'] * width for _ in range(height)]
        # координаты и размер доски в данный момент
        self.LEFT = (1280 - 30 * 16) // 2
        self.TOP = 10
        self.CELL_SIZE = 30
        self.width = width
        self.height = height
        # колонка и ряд в данный момент
        self.board_row = 0
        self.board_col = 0
        # курсор объектов и объекты
        self.primary_objects = pg.sprite.Group()
        self.background_objects = pg.sprite.Group()
        self.all_objects_cursor = 0
        # формат: [Название объекта, изображение, тип, обозначение для текстового файла]
        self.all_objects = [
            {'name': 'Road', 'image': 'road.jpg', "obj_type": 'background', 'placeable': True, 'txt_char': '1'},
            {'name': 'Water', 'image': 'water.png', "obj_type": 'background', 'placeable': False, 'txt_char': '2'},
            {'name': 'Grass', 'image': 'grass.png', "obj_type": 'background', 'placeable': True, 'txt_char': '0'},
            {'name': 'Forest', 'image': 'forest.png', "obj_type": 'background', 'placeable': False, 'txt_char': '3'},
            {'name': 'Necropolis', 'image': 'necropolis.png', "obj_type": 'primary', 'placeable': False,
             'txt_char': '2'},
            {'name': 'Gold', 'image': 'gold.png', "obj_type": 'primary', 'placeable': False, 'txt_char': '1'},
            {'name': 'Player 1', 'image': 'player1.png', "obj_type": 'spawnpoint', 'placeable': False, 'txt_char': 'q'},
            {'name': 'Player 2', 'image': 'player2.png', "obj_type": 'spawnpoint', 'placeable': False, 'txt_char': 'w'},
        ]
        # кнопки
        self.buttonup = PgButton((self.LEFT + 16 * self.CELL_SIZE + 70, 160), (60, 20), load_image('arrowbtnup.jpg'))
        self.buttondown = PgButton((self.LEFT + 16 * self.CELL_SIZE + 70, 280), (60, 20),
                                   load_image('arrowbtndown.jpg'))
        self.savebutton = PgButton((self.LEFT + 16 * self.CELL_SIZE + 60, 500), (80, 40), load_image('savebutton.jpg'))

    def render_interface(self, surface):
        f = pg.font.Font(None, 18)
        # загрузка фонового изображения
        surface.blit(load_image('MapGeneratorInterface.jpg'), (0, 0))
        # отрисовка кнопок и элементов для взаимодействия
        pg.draw.rect(surface, (0, 0, 0), (self.LEFT + 16 * self.CELL_SIZE + 70, 200,
                                          60, 60))  # черный прямоугольник-рамка для объекта
        img = pg.transform.scale(load_image(self.all_objects[self.all_objects_cursor]['image']),
                                 (60, 60))  # объект из списка
        name = f.render(f"name: {self.all_objects[self.all_objects_cursor]['name']}", 1, (0, 0, 0))
        type = f.render(f"type: {self.all_objects[self.all_objects_cursor]['obj_type']}", 1, (0, 0, 0))
        surface.blit(img, (self.LEFT + 16 * self.CELL_SIZE + 70, 200))
        surface.blit(name, (self.LEFT + 16 * self.CELL_SIZE + 60, 185))
        surface.blit(type, (self.LEFT + 16 * self.CELL_SIZE + 60, 265))
        # текст разный
        info = f.render('WASD - перемещение по карте', 1, (0, 0, 0))
        info1 = f.render('ПКМ - удалить primary объект', 1, (0, 0, 0))
        info2 = f.render('ЛКМ - разместить объект', 1, (0, 0, 0))
        info3 = f.render('SAVE - сохранить карту', 1, (0, 0, 0))
        if any('q' in i for i in self.txt_primary_map) and any('w' in j for j in self.txt_primary_map):
            info4 = f.render('Можно сохранить карту', 1, (0, 0, 0))
        else:
            info4 = f.render('Не установлены спавнпоинты', 1, (0, 0, 0))
        surface.blit(info, (self.LEFT - 205, 50))
        surface.blit(info1, (self.LEFT - 205, 70))
        surface.blit(info2, (self.LEFT - 205, 90))
        surface.blit(info3, (self.LEFT - 205, 110))
        surface.blit(info4, (self.LEFT + 16 * self.CELL_SIZE + 11, 550))
        # отрисовка кнопок
        self.buttonup.draw_button(surface)
        self.buttondown.draw_button(surface)
        self.savebutton.draw_button(surface)
        self.draw_minimap(surface)

    def move_sprites(self):
        for i in self.primary_objects:
            i.kill()
        for i in self.background_objects:
            i.kill()
        for row in range(self.board_row, self.board_row + 16):
            for col in range(self.board_col, self.board_col + 16):
                if self.primary_board[row][col] != '*':
                    self.primary_board[row][col].rect.x = (self.primary_board[row][col].pos[
                                                               1] - self.board_col) * 30 + self.LEFT
                    self.primary_board[row][col].rect.y = (self.primary_board[row][col].pos[
                                                               0] - self.board_row) * 30 + self.TOP
                    if (self.board_row <= self.primary_board[row][col].pos[0] < self.board_row + 16 and
                            self.board_col <= self.primary_board[row][col].pos[1] < self.board_col + 16):
                        self.primary_objects.add(self.primary_board[row][col])
                self.background_board[row][col].rect.x = (self.background_board[row][col].pos[
                                                              1] - self.board_col) * 30 + self.LEFT
                self.background_board[row][col].rect.y = (self.background_board[row][col].pos[
                                                              0] - self.board_row) * 30 + self.TOP
                if (self.board_row <= self.background_board[row][col].pos[0] < self.board_row + 16 and
                        self.board_col <= self.background_board[row][col].pos[1] < self.board_col + 16):
                    self.background_objects.add(self.background_board[row][col])

    def add_object(self, cell):
        if cell is not None:
            if self.all_objects[self.all_objects_cursor]['obj_type'] == 'primary':
                if self.background_board[cell[0]][cell[1]].placeable:
                    self.primary_board[cell[0]][cell[1]] = GameObject(
                        ((cell[1]) * 30 + self.LEFT, (cell[0]) * 30 + self.TOP),
                        (cell[0], cell[1]),
                        **self.all_objects[self.all_objects_cursor])
                self.txt_primary_map[cell[0]][cell[1]] = self.all_objects[self.all_objects_cursor]['txt_char']
            elif self.all_objects[self.all_objects_cursor]['obj_type'] == 'background':
                if (self.all_objects[self.all_objects_cursor]['placeable'] or
                        self.primary_board[cell[0]][cell[1]] == '*'):
                    self.background_board[cell[0]][cell[1]] = GameObject((
                        cell[1] * 30 + self.LEFT, cell[0] * 30 + self.TOP),
                        (cell[0], cell[1]),
                        **self.all_objects[self.all_objects_cursor])
                self.txt_background_map[cell[0]][cell[1]] = self.all_objects[self.all_objects_cursor]['txt_char']
            elif self.all_objects[self.all_objects_cursor]['obj_type'] == 'spawnpoint':
                if (self.background_board[cell[0]][cell[1]].placeable and
                        self.primary_board[cell[0]][cell[1]] == '*'):
                    for i in range(self.height):
                        for j in range(self.width):
                            if self.primary_board[i][j] != '*':
                                if (self.primary_board[i][j].txt_char == self.all_objects[self.all_objects_cursor][
                                    'txt_char']):
                                    self.primary_board[i][j] = '*'
                                    self.txt_primary_map[i][j] = '*'
                    self.primary_board[cell[0]][cell[1]] = GameObject(
                        ((cell[1]) * 30 + self.LEFT, (cell[0]) * 30 + self.TOP),
                        (cell[0], cell[1]),
                        **self.all_objects[self.all_objects_cursor])
                    self.txt_primary_map[cell[0]][cell[1]] = self.all_objects[self.all_objects_cursor]['txt_char']

    def del_object(self, pos):
        cell = self.get_cell(pos)
        for i in self.primary_objects:
            if i.pos[1] == cell[1] and i.pos[0] == cell[0]:
                i.kill()
                self.primary_board[cell[0]][cell[1]] = '*'
                self.txt_primary_map[cell[0]][cell[1]] = '*'

    def get_cell(self, pos):
        x, y = pos
        if (self.LEFT < x < 16 * self.CELL_SIZE + self.LEFT and
                self.TOP < y < 16 * self.CELL_SIZE + self.TOP):
            row = (y - self.TOP) // self.CELL_SIZE + self.board_row
            col = (x - self.LEFT) // self.CELL_SIZE + self.board_col
            return row, col

    def buttons_func(self, pos):
        if self.buttonup.check_hit(pos):
            self.all_objects_cursor = max(0, self.all_objects_cursor - 1)
        elif self.buttondown.check_hit(pos):
            self.all_objects_cursor = min(len(self.all_objects) - 1, self.all_objects_cursor + 1)
        elif self.savebutton.check_hit(pos):
            self.save_map()

    def save_map(self):
        self.name = None
        if any('q' in i for i in self.txt_primary_map) and any('w' in i for i in self.txt_primary_map):
            self.root = Tk()
            self.entry = Entry()
            self.entry.pack(pady=10)
            Button(text='Ввести', command=self.check).pack()
            self.label = Label(height=1)
            self.label.pack()
            self.root.mainloop()
        if self.name is not None:
            # общий список карт
            f = open(f"maps/maplist.txt", 'r', encoding='utf8')
            lis = list(map(lambda x: x.strip('\n'), f.readlines()))
            f.close()
            f = open(f"maps/maplist.txt", 'w', encoding='utf8')
            if self.name not in lis:
                lis.append(self.name)
            f.write('\n'.join(lis))
            f.close()
            # объекты переднего плана
            f = open(f"maps/{self.name}_primary.txt", 'w', encoding='utf8')
            f.write('\n'.join([''.join([i for i in j]) for j in self.txt_primary_map]))
            f.close()
            # объекты заднего плана
            f = open(f"maps/{self.name}_background.txt", 'w', encoding='utf8')
            f.write('\n'.join([''.join([i for i in j]) for j in self.txt_background_map]))
            f.close()
            # картинка карты
            fon = Image.new("RGBA", (self.height * 60, self.width * 60), (0, 0, 0))
            for i in range(self.height):
                for j in range(self.width):
                    bpic = Image.open(f'generatorFiles/{self.background_board[i][j].img_name}').convert("RGBA")
                    bpic = bpic.resize((60, 60))
                    fon.paste(bpic, (j * 60, i * 60), bpic)
            fon.save(f"maps/{self.name}_image.png")

    def check(self):
        answer = mb.askyesno(title="Внимание", message="Ввести это название?")
        if answer == True:
            self.name = self.entry.get()
            self.entry.delete(0, END)
            self.root.destroy()

    def draw_minimap(self, surf):
        pass


def run_mapgenerator():
    pg.init()
    size = 1280, 720
    screen = pg.display.set_mode(size)
    clock = pg.time.Clock()
    board = Board(32, 32)
    board.render_interface(screen)
    pg.display.flip()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.add_object(board.get_cell(event.pos))
                    board.buttons_func(event.pos)
                if event.button == 3:
                    board.del_object(event.pos)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    board.board_row = max(board.board_row - 1, 0)
                elif event.key == pg.K_s:
                    board.board_row = min(board.board_row + 1, board.height - 16)
                elif event.key == pg.K_a:
                    board.board_col = max(board.board_col - 1, 0)
                elif event.key == pg.K_d:
                    board.board_col = min(board.board_col + 1, board.width - 16)
        board.render_interface(screen)
        board.move_sprites()
        board.background_objects.draw(screen)
        board.primary_objects.draw(screen)
        pg.display.flip()
        clock.tick(25)

    pg.quit()
run_mapgenerator()