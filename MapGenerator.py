import pygame as pg
import os

pg.init()


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


class Button:
    def __init__(self, xy, wh, image):
        self.xy = xy
        self.wh = wh
        self.image = pg.transform.scale(image, wh)

    def draw_button(self, surface):
        surface.blit(self.image, (self.xy[0], self.xy[1]))

    def check_hit(self, pos):
        return self.xy[0] <= pos[0] <= self.xy[0] + self.wh[0] and self.xy[1] <= pos[1] <= self.xy[1] + self.wh[1]


class GameObject(pg.sprite.Sprite):  # класс спрайтов
    def __init__(self, cords, pos, img):
        super().__init__()
        self.pos = pos
        self.image = pg.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = cords[0]
        self.rect.y = cords[1]


class Board:
    def __init__(self, width, height):
        # все доски и текстовое представление
        self.primary_board = [['*'] * width for _ in range(height)]
        self.background_board = [[GameObject((
            i * 30 + (1280 - 30 * 16) // 2, j * 30 + 10),
            (j, i),
            load_image('road.jpg')) for i in range(width)] for j in range(height)]
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
        self.all_objects = [('Castle', load_image('castle.png', -1), 'primary', '2'),
                            ('Road', load_image('road.jpg'), 'background', '0'),
                            ('Grass', load_image('grass.jpg'), 'background', '1')]
        # кнопки
        self.buttonup = Button((self.LEFT + 16 * self.CELL_SIZE + 70, 170), (60, 20), load_image('arrowbtnup.jpg'))
        self.buttondown = Button((self.LEFT + 16 * self.CELL_SIZE + 70, 270), (60, 20), load_image('arrowbtndown.jpg'))
        self.savebutton = Button((self.LEFT + 16 * self.CELL_SIZE + 60, 500), (80, 40), load_image('savebutton.jpg'))
        # self.infobutton = Button((x, y), (30, 30), load_image('infobutton.jpg'))

    def render_interface(self, surface):
        # загрузка фонового изображения
        surface.blit(load_image('MapGeneratorInterface.jpg'), (0, 0))
        # отрисовка кнопок и элементов для взаимодействия
        pg.draw.rect(surface, (0, 0, 0), (self.LEFT + 16 * self.CELL_SIZE + 70, 200,
                                          60, 60))  # черный прямоугольник-рамка для объекта
        img = pg.transform.scale(self.all_objects[self.all_objects_cursor][1], (60, 60))  # объект из списка
        surface.blit(img, (self.LEFT + 16 * self.CELL_SIZE + 70, 200))

        self.buttonup.draw_button(surface)
        self.buttondown.draw_button(surface)
        self.savebutton.draw_button(surface)

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
            if self.all_objects[self.all_objects_cursor][2] == 'primary':
                self.primary_board[cell[0]][cell[1]] = GameObject(
                    ((cell[1]) * 30 + self.LEFT, (cell[0]) * 30 + self.TOP),
                    (cell[0], cell[1]),
                    self.all_objects[self.all_objects_cursor][1])
                for i in self.primary_objects:
                    if i.pos[1] == cell[1] and i.pos[0] == cell[0]:
                        i.kill()
                self.primary_objects.add(self.primary_board[cell[0]][cell[1]])
                self.txt_primary_map[cell[0]][cell[1]] = self.all_objects[self.all_objects_cursor][-1]
            else:
                self.background_board[cell[0]][cell[1]] = GameObject((
                    cell[1] * 30 + self.LEFT, cell[0] * 30 + self.TOP),
                    (cell[0], cell[1]),
                    self.all_objects[self.all_objects_cursor][1])
                for i in self.background_objects:
                    if i.pos[1] == cell[1] and i.pos[0] == cell[0]:
                        i.kill()
                self.background_objects.add(self.background_board[cell[0]][cell[1]])
                self.txt_background_map[cell[0]][cell[1]] = self.all_objects[self.all_objects_cursor][-1]

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


def run():
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
        clock.tick(5)

    pg.quit()


run()
