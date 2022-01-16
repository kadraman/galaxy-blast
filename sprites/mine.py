import pygame as pg

import constants
from modules.sprite_sheet import SpriteSheet

# maximum intervals before mine is automatically destroyed
MAX_MINE_DISPLAY = 750

class Mine(pg.sprite.Sprite):
    def __init__(self, sprites, x_velocity, y_velocity):
        super(Mine, self).__init__()
        self.timer = 0
        self.interval = 4
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.exploded = False
        self.exploding = False

        self.number_of_images = 1
        sprites = SpriteSheet('./assets/images/mine-1.png')
        self.images = sprites.load_strip([0, 0, 11, 11], 1, -1)

        sprites = SpriteSheet('./assets/images/explosion-1.png')
        self.images.append(sprites.image_at([0, 0, 32, 32], -1))
        sprites = SpriteSheet('./assets/images/explosion-2.png')
        self.images.append(sprites.image_at([0, 0, 32, 32], -1))
        sprites = SpriteSheet('./assets/images/explosion-3.png')
        self.images.append(sprites.image_at([0, 0, 32, 32], -1))

        '''
        self.images = sprites.load_strip([
            constants.SS_MISSILE_X,
            constants.SS_MISSILE_Y,
            constants.SS_MISSILE_WIDTH,
            constants.SS_MISSILE_HEIGHT], self.number_of_images, -1)
        '''

        # scale image for enhanced retro effect!
        for index, image in enumerate(self.images):
            self.images[index] = pg.transform.scale(image, (16, 16))
        self.base_image = self.images[0]

        self.surface = self.images[0]
        self.rect = self.surface.get_rect(
            center=(constants.SCREEN_WIDTH / 2,
                    constants.SCREEN_HEIGHT - 20))
        self.image_index = 0
        self.rotation = 0

    def update(self, dt):
        self.timer += 1
        if self.timer % self.interval == 0:
            self.rotation += 45
        if self.rotation >= MAX_MINE_DISPLAY:
            self.rotation = 0
        self.rect.move_ip(self.x_velocity * dt, self.y_velocity * dt)

        # kill mine after certain period
        if self.timer > self.mine_display_interval:
            if self.image_index == 3:
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
