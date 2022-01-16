import pygame as pg

from modules.misc_utils import safe_division
from modules.sprite_sheet import SpriteSheet

from sprites.base_enemy import BaseEnemy, EnemyType

import constants


class MinionEnemy(BaseEnemy):
    def __init__(self, enemy_type, sprites, player_center, enemy_center, x_velocity, y_velocity, number_of_images,
                 scaled_width, scaled_height):
        super(MinionEnemy, self).__init__(enemy_type, sprites, player_center, enemy_center, x_velocity, y_velocity,
                                          number_of_images,
                                          scaled_width, scaled_height)

        self.player_center = [player_center[0], player_center[1]]
        self.x_start = enemy_center[0]
        self.y_start = enemy_center[1]
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.original_y_velocity = y_velocity
        if enemy_type == EnemyType.MINION_1:
            self.points = 1
        elif enemy_type == EnemyType.MINION_2:
            self.points = 2
        elif enemy_type == EnemyType.MINION_3:
            self.points = 5
        else:
            self.points = 0
        self.join()

    def get_event(self, event, controller):
        pass

    # def update(self, dt):

    def get_surface(self):
        if self.enemy_type == EnemyType.MINION_1:
            image = self.images[self.image_index]
        elif self.enemy_type == EnemyType.MINION_2:
            image = self.images[self.image_index + 2]
        else:
            image = self.images[self.image_index + 4]
        if self.joining:
            return pg.transform.scale(image,
                                      (int(constants.MINION_ENEMY_WIDTH * (self.join_count / 3)),
                                       int(constants.MINION_ENEMY_HEIGHT * (self.join_count / 3))))
        else:
            return image

    def load_images(self):
        sprites = SpriteSheet('./assets/images/enemy_1_ship-2.png')
        images = sprites.load_strip([0, 0, 10, 10], 1, -1)
        sprites = SpriteSheet('./assets/images/enemy_1_ship-1.png')
        images.append(sprites.image_at([0, 0, 10, 10], -1))

        sprites = SpriteSheet('./assets/images/enemy_2_ship-2.png')
        images.append(sprites.image_at([0, 0, 10, 11], 1))
        sprites = SpriteSheet('./assets/images/enemy_2_ship-1.png')
        images.append(sprites.image_at([0, 0, 10, 11], -1))

        sprites = SpriteSheet('./assets/images/enemy_3_ship-2.png')
        images.append(sprites.image_at([0, 0, 13, 8], 1))
        sprites = SpriteSheet('./assets/images/enemy_3_ship-1.png')
        images.append(sprites.image_at([0, 0, 13, 8], -1))
        return images

    def enemy_controller_join(self, dt):
        self.join_count += 1
        if self.join_count > 3:
            self.joining = False
            self.controller_function = self.enemy_controller_pan
        else:
            self.rect.clamp_ip(pg.Rect((self.x_start, self.y_start), (self.rect.width, self.rect.height)))

    def enemy_controller_pan(self, dt):
        if self.timer % 5 == 0:
            self.x_velocity *= -1
        self.rect.move_ip(self.x_velocity * dt, 0)

    def enemy_controller_dive(self, dt):
        if self.rect.bottom > (constants.SCREEN_HEIGHT - self.rect.height) or \
                self.rect.right >= (constants.SCREEN_WIDTH - self.rect.width) or \
                self.rect.left < 0:
            self.rect.clamp_ip(pg.Rect((self.x_start, self.y_start), (self.rect.width, self.rect.height)))
            self.attacking = False
            self.y_velocity = self.original_y_velocity
            self.controller_function = self.enemy_controller_pan
        else:
            self.attacking = True
            if self.enemy_type == EnemyType.MINION_3:
                dx = self.player_center[0] - self.rect.centerx
                dy = self.player_center[1] - self.rect.centery
                number_of_steps = safe_division(dy, self.y_velocity)
                x_velocity = safe_division(dx, number_of_steps)
            else:
                x_velocity = self.x_velocity
            self.rect.move_ip(x_velocity * dt, self.y_velocity * dt)
            self.y_velocity *= 1.01

    def join(self):
        self.controller_function = self.enemy_controller_join

    def attack(self):
        self.controller_function = self.enemy_controller_dive
