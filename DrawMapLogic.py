from Bioms import *
import os


# Загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data/lvls/', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Загрузка уровней
def load_level(filename):
    filename = "data/lvls/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('1'), Травой
    return list(map(lambda x: x.ljust(max_width, '1'), level_map))


# Генерирует неподвижную картинку фона
def generate_background(options):
    pass

