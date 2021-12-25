import pygame as pg

from modules.display_utils import BackGround

from .base_state import BaseState

import constants


class Credits(BaseState):
    def __init__(self):
        super(Credits, self).__init__()
        self.title = self.font.render("You Won", True, pg.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.instructions = self.font.render(constants.TXT_CREDITS,
                                             True, pg.Color("white"))
        instructions_center = (
            self.screen_rect.center[0], self.screen_rect.center[1] + 50)
        self.instructions_rect = self.instructions.get_rect(
            center=instructions_center)

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = pg.Color(color)

    def get_event(self, event):
        self.game_choice(event)

    def draw(self, surface):
        background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        surface.fill([255, 255, 255])
        surface.blit(background.image, background.rect)
        surface.blit(self.instructions, self.instructions_rect)
