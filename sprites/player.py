import pygame as pg

import constants
from modules.sprite_sheet import SpriteSheet


class Player(pg.sprite.Sprite):
    def __init__(self, sprites, velocity, scaled_width, scaled_height):
        super(Player, self).__init__()
        self.sprites = sprites
        self.velocity = velocity
        self.scaled_width = scaled_width
        self.scaled_height = scaled_height
        self.timer = 0
        self.interval = 5
        # self.velocity = 100

        self.number_of_images = 3
        self.images = self.sprites.load_strip([constants.SS_PLAYER_X_1,
                                               constants.SS_PLAYER_Y_1,
                                               constants.SS_PLAYER_WIDTH,
                                               constants.SS_PLAYER_HEIGHT], 1, -1)
        self.images.append(self.sprites.image_at([constants.SS_PLAYER_X_2,
                                                  constants.SS_PLAYER_Y_2,
                                                  constants.SS_PLAYER_WIDTH,
                                                  constants.SS_PLAYER_HEIGHT], -1))
        self.images.append(self.sprites.image_at([constants.SS_PLAYER_X_3,
                                                  constants.SS_PLAYER_Y_3,
                                                  constants.SS_PLAYER_WIDTH,
                                                  constants.SS_PLAYER_HEIGHT], -1))

        # scale image for enhanced retro effect!
        for index, image in enumerate(self.images):
            self.images[index] = pg.transform.scale(image, (self.scaled_width, self.scaled_height))

        self.surface = self.images[0]
        self.rect = self.surface.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 40))
        self.image_index = 0
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_moving_up = False
        self.is_moving_down = False
        self.is_shooting = False

    def get_event(self, event):
        pass

    def update(self, dt):
        self.timer += 1

        if self.is_moving_left:
            self.rect.move_ip(-1 * (self.velocity * dt), 0)
        if self.is_moving_right:
            self.rect.move_ip(self.velocity * dt, 0)
        if self.is_moving_up:
            self.rect.move_ip(0, -1 * (self.velocity * dt))
        if self.is_moving_down:
            self.rect.move_ip(0, self.velocity * dt)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > constants.SCREEN_WIDTH:
            self.rect.right = constants.SCREEN_WIDTH
        if self.rect.top < 50:
            self.rect.top = 0
        if self.rect.bottom > constants.SCREEN_HEIGHT:
            self.rect.bottom = constants.SCREEN_HEIGHT

    def get_surface(self):
        if self.timer % self.interval == 0:
            self.image_index += 1
            if self.image_index >= self.number_of_images:
                self.image_index = 0
        return self.images[self.image_index]
