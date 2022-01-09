import pygame as pg

from random import seed
from random import randint

from modules.sprite_sheet import SpriteSheet

import constants


class Enemy(pg.sprite.Sprite):
    def __init__(self, sprites, center):
        super(Enemy, self).__init__()
        self.timer = 0
        self.interval = 2
        self.join_count = 1
        self.x_velocity = 100
        self.y_velocity = 100
        self.joining = True
        self.attacking = False

        self.number_of_images = 2
        sprites = SpriteSheet('./assets/images/enemy_1_ship-2.png')
        self.images = sprites.load_strip([0, 0, 10, 10], 1, -1)
        sprites = SpriteSheet('./assets/images/enemy_1_ship-1.png')
        self.images.append(sprites.image_at([0, 0, 10, 10], -1))

        '''
        self.number_of_images = constants.SS_ENEMY1_IMAGES
        self.images = sprites.load_strip([
            constants.SS_ENEMY1_X,
            constants.SS_ENEMY1_Y,
            constants.SS_ENEMY1_WIDTH,
            constants.SS_ENEMY1_HEIGHT], self.number_of_images, -1)
        '''

        # scale image for enhanced retro effect!
        for index, image in enumerate(self.images):
            self.images[index] = pg.transform.scale(image, (constants.ENEMY_1_WIDTH, constants.ENEMY_1_HEIGHT))

        self.base_image = self.images[0]
        self.surface = self.images[0]
        self.rect = self.surface.get_rect(center=center)
        self.image_index = 0
        self.screen_rect = pg.display.get_surface().get_rect()
        self.controller_function = self.enemy_controller_join

    def get_event(self, event, joystick):
        pass

    def update(self, dt):
        self.timer += 1
        if self.timer % self.interval == 0:
            self.image_index += 1
        if self.image_index >= self.number_of_images:
            self.image_index = 0

        self.controller_function(dt)

    def enemy_controller_join(self, dt):
        self.join_count += 1
        if self.join_count > 3:
            self.joining = False
            self.controller_function = self.enemy_controller_pan
        else:
            self.rect.clamp_ip(pg.Rect((self.rect.left, 40), (self.rect.width, self.rect.height)))

    def enemy_controller_pan(self, dt):
        if self.timer % 5 == 0:
            self.x_velocity *= -1
        self.rect.move_ip(self.x_velocity * dt, 0)

    def enemy_controller_dive(self, dt):
        if self.rect.bottom > (constants.SCREEN_HEIGHT - self.rect.height):
            self.rect.clamp_ip(pg.Rect((self.rect.left, 40), (self.rect.width, self.rect.height)))
            self.y_velocity = 100
            self.attacking = False
            self.controller_function = self.enemy_controller_pan
        else:
            self.rect.move_ip(0, self.y_velocity * dt)

        self.y_velocity *= 1.01

    def has_landed(self):
        if self.rect.bottom >= self.screen_rect.bottom or self.rect.top <= 0:
            return True

    def is_attacking(self):
        return self.attacking

    def attack(self):
        self.attacking = True
        self.controller_function = self.enemy_controller_dive

    def get_surface(self):
        if self.joining:
            image = self.images[self.image_index]
            return pg.transform.scale(self.images[self.image_index],
                                      (int(constants.ENEMY_1_WIDTH * (self.join_count / 3)),
                                       int(constants.ENEMY_1_HEIGHT * (self.join_count / 3))))
        else:
            return self.images[self.image_index]
