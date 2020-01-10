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
        self.board_row = 0
        self.board_col = 0

    #  self.image_dict = {'1': (load_image('grass.jpg'))}

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render_interface(self, scr):
        # отрисовка пустого поля-сетки
        for i in range(16):
            for j in range(16):
                pg.draw.rect(scr, (160, 160, 160), (self.left + j * self.cell_size,
                                                    self.top + i * self.cell_size, self.cell_size, self.cell_size), 1)
                img = load_image('road.jpg')
                img = pg.transform.scale(img, (28, 28))
                screen.blit(img, (self.left + j * self.cell_size + 1, self.top + i * self.cell_size + 1))

    def render_sprites(self):
        for i in object_sprites:
            if not (self.board_row <= i.pos[0] <= self.board_row + 16 and self.board_col <= i.pos[1] <= self.board_col):
                print(i.pos)
                i.kill()
        for row in range(self.board_row, self.board_row + 16):
            for col in range(self.board_col, self.board_col + 16):
                if self.board[row][col] != '*':
                    print(self.board[row][col])
                    object_sprites.add(self.board[row][col])

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell)
        if cell is not None:
            self.board[cell[0]][cell[1]] = Castle(xy=(cell[1] * 30 + self.left, cell[0] * 30 + self.top), pos=cell)
            object_sprites.add(self.board[cell[0]][cell[1]])

    def get_cell(self, pos):
        x, y = pos
        if (self.left < x < self.width * self.cell_size + self.left and
                self.top < y < self.height * self.cell_size + self.top):
            row = (y - self.top) // self.cell_size + self.board_row
            col = (x - self.left) // self.cell_size + self.board_col
            return row, col


size = 1280, 720
screen = pg.display.set_mode(size)
clock = pg.time.Clock()
object_sprites = pg.sprite.Group()
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                board.board_row = max(board.board_col - 1, 0)
            elif event.key == pygame.K_s:
                board.board_row = min(board.board_row + 1, board.height - 16)
            elif event.key == pygame.K_a:
                board.board_col = max(board.board_col - 1, 0)
            elif event.key == pygame.K_d:
                board.board_col = min(board.board_col + 1, board.width - 16)
    board.render_interface(screen)
    board.render_sprites()
    object_sprites.draw(screen)
    pg.display.flip()
    clock.tick(15)

pg.quit()
