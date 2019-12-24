import pygame


class TextWindow(pygame.sprite.Sprite()):
    def __init__(self, text):
        self.text = text

    def draw(self, screen):
        w, h = pygame.display.get_surface()
        tl_c = w // 4, h // 4
        width = w // 2
        height = h // 2
        pygame.draw.rect(screen, pygame.Color('green'), (tl_c[0], tl_c[1], width, height))
        font = pygame.font.Font(None, 36)
        self.text = font.render(self.text, 1, (0, 0, 0))
        screen.blit(self.text, (tl_c[0] - 10, tl_c[1] - 10))
        pygame.display.update()







