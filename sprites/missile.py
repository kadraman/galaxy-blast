import math
import pygame as pg

import constants


class Missile(pg.sprite.Sprite):
    def __init__(self, sprites, xSpeed, ySpeed):
        super(Missile, self).__init__()
        self.timer = 0
        self.interval = 2
        self.number_of_images = constants.SS_MISSILE_IMAGES
        self.ySpeed = ySpeed
        self.xSpeed = xSpeed
        self.images = sprites.load_strip([
            constants.SS_MISSILE_X,
            constants.SS_MISSILE_Y,
            constants.SS_MISSILE_WIDTH,
            constants.SS_MISSILE_HEIGHT], self.number_of_images, -1)
        self.surface = self.images[0]
        self.rect = self.surface.get_rect(
            center=(constants.SCREEN_WIDTH / 2,
                    constants.SCREEN_HEIGHT - 20))
        self.image_index = 0
        self.rotation = 0

        if self.ySpeed > 0:
            self.rotation = math.degrees(math.atan2(xSpeed, ySpeed)) + 180

    def update(self, keys):
        self.timer += 1
        self.rect.move_ip(self.xSpeed, self.ySpeed)

        if self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

    def get_event(self, event):
        pass

    def get_surface(self):
        if self.timer % self.interval == 0:
            self.image_index += 1
        if self.image_index >= self.number_of_images:
            self.image_index = 0

        rotated_image = pg.transform.rotate(self.images[self.image_index], self.rotation)
        self.rect = rotated_image.get_rect(center=self.rect.center)

        return rotated_image
