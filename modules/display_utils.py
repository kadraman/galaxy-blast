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


class FancyText:
    def __init__(self, font_name, font_size, start_color):
        self.font = pygame.font.Font(font_name, font_size)
        self.color_speed = 5
        self.color_direction = [-1, -1, -1]
        self.start_color = start_color
        self.current_colour = start_color
        self.min_color = 0
        self.max_color = 255

    def draw(self, screen, text_string, x, y):
        text_bitmap = self.font.render(text_string, True, self.current_colour)
        text_rect = text_bitmap.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_bitmap, text_rect)

    def update(self):
        for i in range(3):
            self.current_colour[i] += self.color_speed * self.color_direction[i]
            if self.current_colour[i] >= self.max_color or self.current_colour[i] <= self.min_color:
                self.color_direction[i] *= -1


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
