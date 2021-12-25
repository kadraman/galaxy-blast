import pygame as pg

from .base_state import BaseState

from modules.display_utils import BackGround

import constants


class SplashScreen(BaseState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.title = self.font.render(constants.TITLE, True, pg.Color("blue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = pg.Color("black")
        self.persist["background"] = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        self.next_state = "MAIN_MENU"
        self.time_active = 0

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = color
        background = self.persist["background"]
        self.background = background

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            self.done = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True

    def draw(self, surface):
        surface.fill([255, 255, 255])
        surface.blit(self.background.image, self.background.rect)
        surface.blit(self.title, self.title_rect)

    def update(self, dt):
        self.time_active += dt
        # move to main menu automatically
        if self.time_active >= 2000:
            self.done = True
