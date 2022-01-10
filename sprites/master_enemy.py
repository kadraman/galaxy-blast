import pygame as pg

from random import seed
from random import randint

from modules.sprite_sheet import SpriteSheet

from sprites.base_enemy import BaseEnemy

import constants


class MasterEnemy(BaseEnemy):
    def __init__(self, enemy_type, sprites, center, x_velocity, y_velocity, number_of_images, scaled_width, scaled_height):
        super(MasterEnemy, self).__init__(enemy_type, sprites, center, x_velocity, y_velocity, number_of_images,
                                          scaled_width, scaled_height)

        self.screen_trips = 0
        self.max_screen_trips = 1
        self.points = 10
        self.join()

    def get_event(self, event, controller):
        pass

    # def update(self, dt):

    def get_surface(self):
        if self.joining:
            image = self.images[self.image_index]
            return pg.transform.scale(self.images[self.image_index],
                                      (int(constants.MASTER_ENEMY_WIDTH * (self.join_count / 3)),
                                       int(constants.MASTER_ENEMY_HEIGHT * (self.join_count / 3))))
        else:
            return self.images[self.image_index]

    def load_images(self):
        sprites = SpriteSheet('./assets/images/enemy_2_ship-1.png')
        images = sprites.load_strip([0, 0, 15, 14], 1, -1)
        sprites = SpriteSheet('./assets/images/enemy_2_ship-2.png')
        images.append(sprites.image_at([0, 0, 15, 14], -1))
        return images

    def enemy_controller_join(self, dt):
        self.join_count += 1
        if self.join_count > 1:
            self.joining = False
            self.controller_function = self.enemy_controller_pan
        else:
            self.rect.clamp_ip(pg.Rect((self.rect.left, 200), (self.rect.width, self.rect.height)))

    def enemy_controller_pan(self, dt):
        if self.rect.left < self.rect.width or self.rect.right > constants.SCREEN_WIDTH:
            self.x_velocity *= -1
            self.screen_trips += 1
        elif self.screen_trips >= self.max_screen_trips:
            self.leaving = True
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

    def join(self):
        self.controller_function = self.enemy_controller_join

    def attack(self):
        self.controller_function = self.enemy_controller_dive



