# coding: utf-8
import constants

try:
    import pygame
except ImportError:
    raise ImportError('You must install pygame.')


class SoundEffect:
    def __init__(self, file):
        self.sound = None
        self.load(file)

    def load(self, file):
        self.sound = pygame.mixer.Sound(file)

    def play(self):
        pygame.mixer.Sound.play(self.sound)
