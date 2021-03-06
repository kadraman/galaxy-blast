import pygame as pg

import constants
from modules.display_utils import BackGround
from .base_state import BaseState


class Settings(BaseState):
    def __init__(self):
        super(Settings, self).__init__()
        self.active_index = 0
        self.options = ["Display", "Controller", "Main Menu"]
        self.next_state = "MAIN_MENU"

        self.fancy_text_1 = None
        self.fancy_text_2 = None
        self.author = self.default_font.render(constants.AUTHOR, True, pg.Color("blue"))
        self.author_rect = self.author.get_rect(center=self.screen_rect.center)

        self.title = self.title_font.render(constants.TITLE, True, pg.Color("green"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

    def startup(self, persistent):
        self.active_index = 0
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
        self.fancy_text_1 = self.persist["fancy_text_1"]
        self.fancy_text_2 = self.persist["fancy_text_2"]

    def render_text(self, index):
        color = pg.Color("red") if index == self.active_index else pg.Color("white")
        return self.default_font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0],
                  self.screen_rect.center[1] + (index * 50) + 75)
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            self.next_state = "DISPLAY_TEST"
            self.done = True
        elif self.active_index == 1:
            self.next_state = "CONTROLLER_TEST"
            self.done = True
        elif self.active_index == 2:
            self.next_state = "MAIN_MENU"
            self.done = True

    def get_event(self, event, controller):
        self.menu_choice(event, controller)

    def draw(self, surface):
        background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        surface.fill(self.screen_color)
        surface.blit(background.image, background.rect)

        self.fancy_text_1.draw(self.screen, constants.AUTHOR, 320, 75)
        self.fancy_text_2.draw(self.screen, constants.TITLE, 320, 150)

        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(
                text_render, index))

    def update(self, dt):
        self.fancy_text_1.update()
        self.fancy_text_2.update()
