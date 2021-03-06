import math
import pygame as pg

from modules.sprite_sheet import SpriteSheet

import constants


class Missile(pg.sprite.Sprite):
    def __init__(self, sprites, x_velocity, y_velocity, is_player_missile, is_boss_missile):
        super(Missile, self).__init__()
        self.sprites = sprites
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.is_player_missile = is_player_missile
        self.is_boss_missile = is_boss_missile
        self.timer = 0
        self.interval = 5

        self.images = self.sprites.load_strip([constants.SS_MISSILE_X_1,
                                               constants.SS_MISSILE_Y_1,
                                               constants.SS_MISSILE_WIDTH,
                                               constants.SS_MISSILE_HEIGHT], 1, -1)
        self.images.append(self.sprites.image_at([constants.SS_MISSILE_X_2,
                                                  constants.SS_MISSILE_Y_2,
                                                  constants.SS_MISSILE_WIDTH,
                                                  constants.SS_MISSILE_HEIGHT], -1))
        self.images.append(self.sprites.image_at([constants.SS_MISSILE_X_3,
                                                  constants.SS_MISSILE_Y_3,
                                                  constants.SS_MISSILE_WIDTH,
                                                  constants.SS_MISSILE_HEIGHT], -1))

        # scale image for enhanced retro effect!
        for index, image in enumerate(self.images):
            self.images[index] = pg.transform.scale(image, (constants.MISSILE_WIDTH, constants.MISSILE_HEIGHT))
        self.base_image = self.images[0]

        self.surface = self.images[0]
        self.rect = self.surface.get_rect(
            center=(constants.SCREEN_WIDTH / 2,
                    constants.SCREEN_HEIGHT - 20))
        self.image_index = 0
        self.rotation = 0

        if self.y_velocity > 0:
            self.rotation = math.degrees(math.atan2(x_velocity, y_velocity)) + 180

    def update(self, dt):
        self.timer += 1
        if self.is_player_missile:
            self.image_index = 0
        elif self.is_boss_missile:
            self.image_index = 1
        else:
            self.image_index = 2
        self.rect.move_ip(self.x_velocity * dt, self.y_velocity * dt)

        if self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

    def get_event(self, event, controller):
        pass

    def get_surface(self):
        rotated_image = pg.transform.rotate(self.images[self.image_index], self.rotation)
        self.rect = rotated_image.get_rect(center=self.rect.center)

        return rotated_image
