import pygame as pg

import constants
from modules.sprite_sheet import SpriteSheet

# maximum intervals before mine is automatically destroyed
MAX_MINE_DISPLAY = 750


class Mine(pg.sprite.Sprite):
    def __init__(self, sprites, x_velocity, y_velocity, scaled_width, scaled_height):
        super(Mine, self).__init__()
        self.sprites = sprites
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.scaled_width = scaled_width
        self.scaled_height = scaled_height
        self.timer = 0
        self.interval = 5
        self.exploded = False
        self.exploding = False
        self.image_index = 0
        self.rotation = 0
        self.images = self.sprites.load_strip([constants.SS_MINE_X,
                                               constants.SS_MINE_Y,
                                               constants.SS_MINE_WIDTH,
                                               constants.SS_MINE_HEIGHT], 1, -1)
        self.images.append(self.sprites.image_at([constants.SS_EXPLOSION_X_1,
                                                  constants.SS_EXPLOSION_Y_1,
                                                  constants.SS_EXPLOSION_WIDTH,
                                                  constants.SS_EXPLOSION_HEIGHT], -1))
        self.images.append(self.sprites.image_at([constants.SS_EXPLOSION_X_2,
                                                  constants.SS_EXPLOSION_Y_2,
                                                  constants.SS_EXPLOSION_WIDTH,
                                                  constants.SS_EXPLOSION_HEIGHT], -1))
        self.images.append(self.sprites.image_at([constants.SS_EXPLOSION_X_3,
                                                  constants.SS_EXPLOSION_Y_3,
                                                  constants.SS_EXPLOSION_WIDTH,
                                                  constants.SS_EXPLOSION_HEIGHT], -1))
        # scale images for enhanced retro effect!
        if self.scaled_width > 0 and self.scaled_height > 0:
            for index, image in enumerate(self.images):
                self.images[index] = pg.transform.scale(image, (self.scaled_width, self.scaled_height))

        self.base_image = self.images[0]
        self.surface = self.images[0]
        self.rect = self.surface.get_rect(
            center=(constants.SCREEN_WIDTH / 2,
                    constants.SCREEN_HEIGHT - 20))

    def update(self, dt):
        self.timer += 1
        if self.timer % self.interval == 0:
            self.rotation += 45
        if self.rotation >= 360:
            self.rotation = 0
        self.rect.move_ip(self.x_velocity * dt, self.y_velocity * dt)

        # kill mine after certain period
        if self.timer > MAX_MINE_DISPLAY:
            if self.image_index == 3:
                self.exploding = False
                self.kill()
            else:
                self.image_index += 1
                self.exploding = True

    def get_event(self, event, controller):
        pass

    def get_surface(self):
        if self.exploding:
            return self.images[self.image_index]
        else:
            rotated_image = pg.transform.rotate(self.images[self.image_index], self.rotation)
            self.rect = rotated_image.get_rect(center=self.rect.center)

            return rotated_image
