import math
import pygame as pg

from modules.sprite_sheet import SpriteSheet

import constants


class Missile(pg.sprite.Sprite):
    def __init__(self, sprites, x_velocity, y_velocity, is_player_missile):
        super(Missile, self).__init__()
        self.timer = 0
        self.interval = 2
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.is_player_missile = is_player_missile

        self.number_of_images = 2
        sprites = SpriteSheet('./assets/images/missile-1.png')
        self.images = sprites.load_strip([0, 0, 3, 10], 1, -1)
        sprites = SpriteSheet('./assets/images/missile-2.png')
        self.images.append(sprites.image_at([0, 0, 3, 10], -1))

        '''
        self.images = sprites.load_strip([
            constants.SS_MISSILE_X,
            constants.SS_MISSILE_Y,
            constants.SS_MISSILE_WIDTH,
            constants.SS_MISSILE_HEIGHT], self.number_of_images, -1)
        '''

        # scale image for enhanced retro effect!
        for index, image in enumerate(self.images):
            self.images[index] = pg.transform.scale(image, (4, 20))
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
        # if self.timer % self.interval == 0:
        #     self.image_index += 1
        # if self.image_index >= self.number_of_images:
        #     self.image_index = 0
        if self.is_player_missile:
            self.image_index = 0
        else:
            self.image_index = 1
        self.rect.move_ip(self.x_velocity * dt, self.y_velocity * dt)

        if self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

    def get_event(self, event, joystick):
        pass

    def get_surface(self):
        rotated_image = pg.transform.rotate(self.images[self.image_index], self.rotation)
        self.rect = rotated_image.get_rect(center=self.rect.center)

        return rotated_image
