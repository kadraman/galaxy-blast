import pygame as pg

from .base_state import BaseState

from modules.display_utils import BackGround

import constants


class SplashScreen(BaseState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.persist["screen_color"] = pg.Color("black")
        self.persist["background"] = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        self.next_state = "MAIN_MENU"
        self.time_active = 0

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
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            self.done = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
        elif event.type == pg.JOYBUTTONUP:
            self.done = True

    def draw(self, surface):
        background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        surface.fill(self.screen_color)
        surface.blit(background.image, background.rect)
        surface.blit(self.author, (constants.SCREEN_WIDTH / 2 - self.author_rect.width / 2, 150))
        surface.blit(self.title_logo, self.title_logo_rect)

    def update(self, dt):
        self.time_active += dt * 1000
        # move to main menu automatically
        if self.time_active >= 2000:
            self.done = True
