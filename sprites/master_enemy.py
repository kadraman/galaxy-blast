import pygame as pg

from random import seed
from random import randint

from modules.sprite_sheet import SpriteSheet

from sprites.base_enemy import BaseEnemy

import constants


class MasterEnemy(BaseEnemy):
    def __init__(self, enemy_type, sprites, player_rect, center, x_velocity, y_velocity, number_of_images, scaled_width,
                 scaled_height):
        super(MasterEnemy, self).__init__(enemy_type, sprites, player_rect, center, x_velocity, y_velocity,
                                          number_of_images, scaled_width, scaled_height)
        self.screen_trips = 0
        self.max_screen_trips = 1
        self.placed_mine = False
        self.points = 10
        self.join()

    def get_event(self, event, controller):
        pass

    # def update(self, dt):

    def get_surface(self):
        if self.joining:
            return pg.transform.scale(self.images[self.image_index],
                                      (int(self.scaled_width * (self.join_count / 5)),
                                       int(self.scaled_height * (self.join_count / 5))))
        else:
            return self.images[self.image_index]

    def load_images(self):
        images = self.sprites.load_strip([constants.SS_MASTER_ENEMY_X_1,
                                          constants.SS_MASTER_ENEMY_Y_1,
                                          constants.SS_MASTER_ENEMY_WIDTH,
                                          constants.SS_MASTER_ENEMY_HEIGHT], 1, -1)
        images.append(self.sprites.image_at([constants.SS_MASTER_ENEMY_X_2,
                                            constants.SS_MASTER_ENEMY_Y_2,
                                            constants.SS_MASTER_ENEMY_WIDTH,
                                            constants.SS_MASTER_ENEMY_HEIGHT], -1))
        return images

    def enemy_controller_join(self, dt):
        self.join_count += 1
        if self.join_count > 3:
            self.joining = False
            self.controller_function = self.enemy_controller_pan
        else:
            self.rect.clamp_ip(pg.Rect((self.rect.left, self.rect.top), (self.rect.width, self.rect.height)))

    def enemy_controller_pan(self, dt):
        # panning right
        if self.rect.right >= constants.SCREEN_WIDTH and self.x_velocity > 0:
            self.x_velocity *= -1
            self.screen_trips += 1
        # panning left
        if self.rect.left <= 0 and self.x_velocity < 0:
            self.x_velocity *= -1
            self.screen_trips += 1
        # finished screen round trips ?
        if self.screen_trips >= self.max_screen_trips:
            self.kill()
        else:
            self.rect.move_ip(self.x_velocity * dt, 0)

    def enemy_controller_dive(self, dt):
        print("not implemented for this enemy")

    def join(self):
        self.controller_function = self.enemy_controller_join

    def attack(self):
        self.controller_function = self.enemy_controller_dive
