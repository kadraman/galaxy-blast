import pygame as pg

from .base_state import BaseState

from modules.display_utils import BackGround
from modules.display_utils import TextPrint

import constants


class DisplayTest(BaseState):
    def __init__(self):
        super(DisplayTest, self).__init__()
        self.interval = 0
        self.last_press = None
        # self.options = ["Display", "Controller", "Main Menu"]
        self.next_state = "SETTINGS"

    def startup(self, persistent):
        self.interval = 0
        self.last_press = None
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

    def render_text(self, index):
        color = pg.Color("red") if index == self.active_index else pg.Color("white")
        return self.default_font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0],
                  self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)

    def get_event(self, event, controller):
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.next_state = "SETTINGS"
                self.done = True

    def draw(self, surface):
        surface.fill(self.screen_color)

        tp = TextPrint()

        tp.draw(surface, "[Press ESC to stop test]")

        # tp.draw(surface, "Number of joysticks: {}".format(joystick_count))
        # tp.indent()

