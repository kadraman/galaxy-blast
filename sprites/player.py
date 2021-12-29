import pygame as pg
from pygame.locals import (
    K_LEFT,
    K_RIGHT
)

import constants


class Player(pg.sprite.Sprite):
    def __init__(self, sprites):
        super(Player, self).__init__()
        self.timer = 0
        self.interval = 2
        self.number_of_images = constants.SS_PLAYER_IMAGES
        self.images = sprites.load_strip([
            constants.SS_PLAYER_X,
            constants.SS_PLAYER_Y,
            constants.SS_PLAYER_WIDTH,
            constants.SS_PLAYER_HEIGHT], self.number_of_images, -1)

        # scale explosion images to size of enemy images
        for index, image in enumerate(self.images):
            self.images[index] = pg.transform.scale(image, (32, 32))

        self.surface = self.images[0]
        self.rect = self.surface.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 40))
        self.image_index = 0

    def get_event(self, event):
        pass

    def update(self, pressed_keys):
        self.timer += 1

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > constants.SCREEN_WIDTH:
            self.rect.right = constants.SCREEN_WIDTH

    def get_surface(self):
        if self.timer % self.interval == 0:
            self.image_index += 1
            if self.image_index >= self.number_of_images:
                self.image_index = 0
        return self.images[self.image_index]
