import pygame as pg

import constants
from modules.sprite_sheet import SpriteSheet


class Player(pg.sprite.Sprite):
    def __init__(self, sprites):
        super(Player, self).__init__()
        self.timer = 0
        self.interval = 2
        self.velocity = 100

        self.number_of_images = 3
        sprites = SpriteSheet('./assets/images/player_ship-1.png')
        self.images = sprites.load_strip([0, 0, 16, 20], 1, -1)
        sprites = SpriteSheet('./assets/images/player_ship-2.png')
        self.images.append(sprites.image_at([0, 0, 16, 20], -1))
        sprites = SpriteSheet('./assets/images/player_ship-3.png')
        self.images.append(sprites.image_at([0, 0, 16, 20], -1))

        '''
        self.number_of_images = constants.SS_PLAYER_IMAGES
        self.images = sprites.load_strip([
            constants.SS_PLAYER_X,
            constants.SS_PLAYER_Y,
            constants.SS_PLAYER_WIDTH,
            constants.SS_PLAYER_HEIGHT], self.number_of_images, -1)
        '''

        # scale image for enhanced retro effect!
        for index, image in enumerate(self.images):
            self.images[index] = pg.transform.scale(image, (32, 32))

        self.surface = self.images[0]
        self.rect = self.surface.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 40))
        self.image_index = 0
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_shooting = False

    def get_event(self, event):
        pass

    def update(self, dt):
        self.timer += 1

        if self.is_moving_left:
            self.rect.move_ip(-1 * (self.velocity * dt), 0)
        if self.is_moving_right:
            self.rect.move_ip(self.velocity * dt, 0)

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
