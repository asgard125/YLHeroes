import pygame as pg
import os

pg.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('generatorFiles', name)
    image = pg.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class GameObject(pg.sprite.Sprite):
    def __init__(self, cords, pos, img):
        super().__init__()
        self.pos = pos
        self.image = pg.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = cords[0]
        self.rect.y = cords[1]


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_board = [['*'] * width for _ in range(height)]
        self.primary_board = [['*'] * width for _ in range(height)]
        self.txt_primary_map = [['*'] * width for _ in range(height)]
        self.txt_background_map = [['*'] * width for _ in range(height)]
        self.LEFT = (1280 - 30 * 16) // 2
        self.TOP = 10
        self.CELL_SIZE = 30
        self.board_row = 0
        self.board_col = 0
        self.all_objects_cursor = 0
        self.all_objects = [('Castle', load_image('castle.png'), 'primary'),
                            ('Road', load_image('road.jpg'), 'background'),
                            ('Grass', load_image('grass.jpg'), 'background')]

    def render_interface(self, scr):
        # загрузка фонового изображения
        scr.blit(load_image('MapGeneratorInterface.jpg'), (0, 0))
        # отрисовка
        pg.draw.rect(scr, (0, 0, 0), (self.LEFT + 16 * self.CELL_SIZE + 70, 200,
                                      60, 60))
        img = pg.transform.scale(self.all_objects[self.all_objects_cursor][1], (60, 60))
        scr.blit(img, (self.LEFT + 16 * self.CELL_SIZE + 70, 200))

    def render_sprites(self):
        for i in primary_objects:
            if not (self.board_row <= i.pos[0] <= self.board_row + 16 and self.board_col <= i.pos[1] <= self.board_col):
                i.kill()
        for row in range(self.board_row, self.board_row + 16):
            for col in range(self.board_col, self.board_col + 16):
                if self.primary_board[row][col] != '*':
                    primary_objects.add(self.primary_board[row][col])

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell)
        if cell is not None:
            if self.all_objects[self.all_objects_cursor][2] == 'primary':
                self.primary_board[cell[0]][cell[1]] = GameObject((cell[1] * 30 + self.LEFT, cell[0] * 30 + self.TOP),
                                                                  (cell[0] + self.board_row, cell[1] + self.board_col),
                                                                  self.all_objects[self.all_objects_cursor][1])
                primary_objects.add(self.primary_board[cell[0]][cell[1]])
            else:
                self.background_board[cell[0]][cell[1]] = GameObject(
                    (cell[1] * 30 + self.LEFT, cell[0] * 30 + self.TOP),
                    (cell[0] + self.board_row, cell[1] + self.board_col),
                    self.all_objects[self.all_objects_cursor][1])
                background_objects.add(self.primary_board[cell[0]][cell[1]])

    def get_cell(self, pos):
        x, y = pos
        if (self.LEFT < x < self.width * self.CELL_SIZE + self.LEFT and
                self.TOP < y < self.height * self.CELL_SIZE + self.TOP):
            row = (y - self.TOP) // self.CELL_SIZE
            col = (x - self.LEFT) // self.CELL_SIZE
            return row, col


size = 1280, 720
screen = pg.display.set_mode(size)
clock = pg.time.Clock()
primary_objects = pg.sprite.Group()
background_objects = pg.sprite.Group()
board = Board(32, 32)
board.render_interface(screen)
pg.display.flip()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
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
    board.render_sprites()
    background_objects.draw(screen)
    primary_objects.draw(screen)
    pg.display.flip()
    clock.tick(15)

pg.quit()
