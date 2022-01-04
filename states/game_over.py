import pygame as pg

from modules.display_utils import BackGround

from .base_state import BaseState

import constants


class GameOver(BaseState):
    def __init__(self):
        super(GameOver, self).__init__()
        self.title = self.font.render("Game Over", True, pg.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.font2 = pg.font.Font(constants.DEFAULT_FONT, 10)
        self.instructions = self.font2.render(constants.TXT_GAME_OVER,
                                              True, pg.Color("white"))
        instructions_center = (
            self.screen_rect.center[0], self.screen_rect.center[1] + 50)
        self.instructions_rect = self.instructions.get_rect(
            center=instructions_center)

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        try:
            color
        except NameError:
            color = self.default_screen_color
        self.screen_color = color
        background = self.persist["background"]
        try:
            background
        except NameError:
            background = self.default_background
        self.background = background

    def get_event(self, event, joystick):
        self.game_choice(event)

    def draw(self, surface):
        background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        surface.fill([255, 255, 255])
        surface.blit(background.image, background.rect)
        surface.blit(self.title, self.title_rect)
        surface.blit(self.instructions, self.instructions_rect)
