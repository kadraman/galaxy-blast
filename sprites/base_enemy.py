import pygame as pg

import constants


class EnemyType:
    MINION_1 = 1
    MINION_2 = 2
    MINION_3 = 3
    MASTER = 4
    BOSS = 5


class BaseEnemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, sprites, player_center, enemy_center, x_velocity, y_velocity, number_of_images, scaled_width, scaled_height):
        super(BaseEnemy, self).__init__()
        self.sprites = sprites
        self.enemy_type = enemy_type
        self.timer = 0
        self.interval = 5
        self.join_count = 1
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.joining = True
        self.attacking = False
        self.leaving = False
        self.points = 0  # how many points for killing the enemy

        self.number_of_images = number_of_images
        self.images = self.load_images()

        self.scaled_width = scaled_width
        self.scaled_height = scaled_height
        self.scale_images(self.scaled_width, self.scaled_height)

        self.base_image = self.images[0]
        self.surface = self.images[0]
        self.rect = self.surface.get_rect(center=enemy_center)
        self.image_index = 0
        self.screen_rect = pg.display.get_surface().get_rect()

        self.controller_function = self.enemy_controller_static

    def get_event(self, event, controller):
        pass

    def update(self, dt):
        self.timer += 1
        if self.timer % self.interval == 0:
            self.image_index += 1
        if self.image_index >= self.number_of_images:
            self.image_index = 0

        self.controller_function(dt)

    def get_surface(self):
        pass

    def load_images(self):
        pass

    def scale_images(self, scaled_width, scaled_height):
        if self.images is None:
            return
        # scale images for enhanced retro effect!
        if scaled_width > 0 and scaled_height > 0:
            for index, image in enumerate(self.images):
                self.images[index] = pg.transform.scale(image, (scaled_width, scaled_height))

    def at_bottom(self):
        if self.rect.bottom >= self.screen_rect.bottom or self.rect.top <= 0:
            return True

    def is_joining(self):
        return self.joining

    def is_leaving(self):
        return self.leaving

    def is_attacking(self):
        return self.attacking

    def attack(self):
        self.attacking = True
        pass

    def enemy_controller_static(self, dt):
        # do nothing
        return
