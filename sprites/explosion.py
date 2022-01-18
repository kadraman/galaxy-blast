import pygame as pg

from modules.sprite_sheet import SpriteSheet

import constants


class Explosion(pg.sprite.Sprite):
    def __init__(self, sprites, center, size):
        super(Explosion, self).__init__()
        self.sprites = sprites
        self.center = center
        self.size = size
        self.timer = 0
        self.interval = 5

        self.number_of_images = 3
        self.images = self.sprites.load_strip([constants.SS_EXPLOSION_X_1,
                                               constants.SS_EXPLOSION_Y_1,
                                               constants.SS_EXPLOSION_WIDTH,
                                               constants.SS_EXPLOSION_HEIGHT], 1, -1)
        self.images.append(self.sprites.image_at([constants.SS_EXPLOSION_X_2,
                                                  constants.SS_EXPLOSION_Y_2,
                                                  constants.SS_EXPLOSION_WIDTH,
                                                  constants.SS_EXPLOSION_HEIGHT], -1))
        self.images.append(self.sprites.image_at([constants.SS_EXPLOSION_X_3,
                                                  constants.SS_EXPLOSION_Y_3,
                                                  constants.SS_EXPLOSION_WIDTH,
                                                  constants.SS_EXPLOSION_HEIGHT], -1))

        self.base_image = self.images[0]
        self.surface = self.images[0]
        self.rect = self.surface.get_rect(center=self.center)
        self.image_index = 0

    def get_event(self, event, controller):
        pass

    def update(self, dt):
        self.timer += 1
        if self.timer % self.interval == 0:
            self.image_index += 1

        if self.image_index >= self.number_of_images:
            self.kill()

    def get_surface(self):
        return self.images[self.image_index]
