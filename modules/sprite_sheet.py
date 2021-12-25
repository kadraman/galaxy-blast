# coding: utf-8

"""
This module handles sprite sheets
This was taken https://www.pygame.org/wiki/Spritesheet?parent=CookBook
"""

try:
    import pygame
except ImportError:
    raise ImportError('You must install pygame.')


class SpriteSheet(object):

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load sprite sheet image:', filename)
            raise SystemExit(message)

    def image_at(self, rectangle, color_key=None):
        """
        Load a specific image from a specific rectangle
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        return image

    def images_at(self, rects, color_key=None):
        """
        Loads multiple images, supply a list of coordinates
        """
        return [self.image_at(rect, color_key) for rect in rects]

    def load_strip(self, rect, image_count, color_key=None):
        """
        Loads a strip of images and returns them as a list
        """
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, color_key)
