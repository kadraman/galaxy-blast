import pygame as pg

import constants


class Enemy(pg.sprite.Sprite):
    def __init__(self, sprites, center):
        super(Enemy, self).__init__()
        self.timer = 0
        self.interval = 10
        self.x_velocity = 1
        self.number_of_images = constants.SS_ENEMY1_IMAGES
        self.images = sprites.load_strip([
            constants.SS_ENEMY1_X,
            constants.SS_ENEMY1_Y,
            constants.SS_ENEMY1_WIDTH,
            constants.SS_ENEMY1_HEIGHT], self.number_of_images, -1)
        self.surface = self.images[0]
        self.rect = self.surface.get_rect(center=center)
        self.image_index = 0
        self.screen_rect = pg.display.get_surface().get_rect()

    def get_event(self, event):
        pass

    def update(self, pressed_keys):
        self.timer += 1
        self.rect.move_ip(self.x_velocity, 0)

        if (self.rect.right > constants.SCREEN_WIDTH
                or self.rect.left < 0):
            self.x_velocity *= -1.25
            self.rect.top += constants.ENEMY_MOVE_DOWN
            self.rect.clamp_ip(self.screen_rect)

    """
        Check if the enemy has landed
        
        Return True if the sprite has reach the bottom of the screen.
    """
    def has_landed(self):
        if self.rect.bottom >= self.screen_rect.bottom or self.rect.top <= 0:
            return True

    def get_surface(self):
        if self.timer % self.interval == 0:
            self.image_index += 1
            if self.image_index >= self.number_of_images:
                self.image_index = 0

        return self.images[self.image_index]
