import pygame as pg

import constants


class Digit(pg.sprite.Sprite):
    def __init__(self, sprites):
        super(Digit, self).__init__()
        self.timer = 0
        self.interval = 0
        self.number_of_images = constants.SS_DIGIT_IMAGES
        self.images = sprites.images_at(
            [
                [
                    constants.SS_DIGIT0_X,
                    constants.SS_DIGIT0_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGIT1_X,
                    constants.SS_DIGIT1_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGIT2_X,
                    constants.SS_DIGIT2_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGIT3_X,
                    constants.SS_DIGIT3_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGIT4_X,
                    constants.SS_DIGIT4_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGIT5_X,
                    constants.SS_DIGIT5_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGIT6_X,
                    constants.SS_DIGIT6_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGIT7_X,
                    constants.SS_DIGIT7_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGIT8_X,
                    constants.SS_DIGIT8_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGIT9_X,
                    constants.SS_DIGIT9_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ],
                [
                    constants.SS_DIGITX_X,
                    constants.SS_DIGITX_Y,
                    constants.SS_DIGIT_WIDTH,
                    constants.SS_DIGIT_HEIGHT
                ]
            ],
            -1)

        # scale explosion images to size of enemy images
        # for index, image in enumerate(self.images):
        #    self.images[index] = pg.transform.scale(image, (32, 32))

        self.surface = self.images[0]
        self.rect = self.surface.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 40))
        self.image_index = 0

    def get_event(self, event):
        pass

    def update(self, pressed_keys):
        self.timer += 1

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > constants.SCREEN_WIDTH:
            self.rect.right = constants.SCREEN_WIDTH

    def get_surface(self, digit):
        # if self.timer % self.interval == 0:
        #    self.image_index += 1
        #    if self.image_index >= self.number_of_images:
        #        self.image_index = 0
        return self.images[digit]
