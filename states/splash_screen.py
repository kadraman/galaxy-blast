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

        self.author = self.default_font.render(constants.AUTHOR, True, pg.Color("blue"))
        self.author_rect = self.author.get_rect(center=self.screen_rect.center)

        self.title = self.title_font.render(constants.TITLE, True, pg.Color("green"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

        self.intro_sound = pg.mixer.Sound("./assets/sounds/368691__fartbiscuit1700__8-bit-arcade-video-game-start-sound-effect-gun-reload-and-jump.ogg")
        if constants.PLAY_SOUNDS:
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
        surface.blit(self.author, (constants.SCREEN_WIDTH / 2 - self.author_rect.width / 2, 100))
        surface.blit(self.title, (constants.SCREEN_WIDTH / 2 - self.title_rect.width / 2, 150))

    def update(self, dt):
        self.time_active += dt * 1000
        # move to main menu automatically
        if self.time_active >= 2000:
            self.done = True
