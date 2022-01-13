import pygame as pg

from .base_state import BaseState

from modules.display_utils import BackGround, FancyText

import constants


class SplashScreen(BaseState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.persist["screen_color"] = pg.Color("black")
        self.persist["background"] = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        self.next_state = "MAIN_MENU"
        self.time_active = 0

        self.fancy_text_1 = FancyText(constants.DEFAULT_FONT, constants.DEFAULT_FONT_SIZE, [20, 20, 150])
        self.fancy_text_1.color_direction = [0, 0, 1]
        self.fancy_text_1.color_speed = 5

        self.fancy_text_2 = FancyText(constants.TITLE_FONT, constants.TITLE_FONT_SIZE, [20, 150, 20])
        self.fancy_text_2.color_direction = [0, 1, 0]
        self.fancy_text_2.color_speed = 5

        self.intro_sound = pg.mixer.Sound("./assets/sounds/368691__fartbiscuit1700__8-bit-arcade-video-game-start-sound-effect-gun-reload-and-jump.ogg")
        self.intro_sound.play()

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

        persistent["fancy_text_1"] = self.fancy_text_1
        persistent["fancy_text_2"] = self.fancy_text_2

    def get_event(self, event, controller):
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
        self.fancy_text_1.draw(self.screen, constants.AUTHOR, 320, 75)
        self.fancy_text_2.draw(self.screen, constants.TITLE, 320, 150)

    def update(self, dt):
        self.time_active += dt * 1000
        # move to main menu automatically
        if self.time_active >= 2500:
            self.done = True
        self.fancy_text_1.update()
        self.fancy_text_2.update()
