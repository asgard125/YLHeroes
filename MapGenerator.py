import pygame as pg
from Bioms import *

pg.init()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['*'] * width for _ in range(height)]
        self.txt_map = [['*'] * width for _ in range(height)]
        self.left = 400
        self.top = 10
        self.cell_size = 30

    #  self.image_dict = {'1': (load_image('grass.jpg'))}

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scr):
        # отрисовка пустого поля-сетки
        for i in range(self.height):
            for j in range(self.width):
                pg.draw.rect(scr, (160, 160, 160), (self.left + j * self.cell_size,
                                                    self.top + i * self.cell_size, self.cell_size, self.cell_size), 1)
                img = load_image('road.jpg')
                img = pg.transform.scale(img, (28, 28))
                screen.blit(img, (self.left + j * self.cell_size + 1, self.top + i * self.cell_size + 1))
        # отрисовка спрайтов



    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell)
        if cell is not None:
            self.board[cell[0]][cell[1]] = Castle(xy=(cell[1] * 30 + self.left, cell[0] * 30 + self.top))
            object_sprites.add(self.board[cell[0]][cell[1]])

    def get_cell(self, pos):
        x, y = pos
        if (self.left < x < self.width * self.cell_size + self.left and
                self.top < y < self.height * self.cell_size + self.top):
            row = (x - self.left) // self.cell_size
            col = (y - self.top) // self.cell_size
            return col, row


size = 1280, 720
screen = pg.display.set_mode(size)
board = Board(16, 16)
board.render(screen)
pg.display.flip()
running = True
object_sprites = pg.sprite.Group()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    object_sprites.draw(screen)
    pg.display.flip()

pg.quit()
