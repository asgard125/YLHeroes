import pygame as pg

pg.init()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.cl = pg.Color('grey')

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scr):
        for i in range(self.height):
            for j in range(self.width):
                pg.draw.rect(scr, self.cl, (self.left + j * self.cell_size,
                                            self.top + i * self.cell_size, self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

    def get_cell(self, pos):
        x, y = pos
        if self.left < x < self.width * self.cell_size and self.top < y < self.height * self.cell_size:
            row = (x - self.left) // self.cell_size
            col = (y - self.top) // self.cell_size
            return col, row


size = 580, 580
screen = pg.display.set_mode(size)
pg.display.flip()
board = Board(64, 64)
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            print(1)
    screen.fill((0, 0, 0))
    board.render(screen)
    pg.display.flip()

pg.quit()
