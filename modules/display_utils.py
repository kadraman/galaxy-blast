# coding: utf-8
import constants

try:
    import pygame
except ImportError:
    raise ImportError('You must install pygame.')


class BackGround(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file).convert_alpha()
        pygame.transform.scale(self.image,
                               (self.image.get_width() / constants.SCREEN_WIDTH,
                                self.image.get_height() / constants.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class TextPrint:
    def __init__(self):
        self.line_height = None
        self.y = None
        self.x = None
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def draw(self, screen, text_string):
        text_bitmap = self.font.render(text_string, True, constants.WHITE)
        screen.blit(text_bitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10
