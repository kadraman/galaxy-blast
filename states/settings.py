import pygame as pg

from .base_state import BaseState

from modules.display_utils import BackGround

import constants


class Settings(BaseState):
    def __init__(self):
        super(Settings, self).__init__()
        self.active_index = 0
        self.options = ["Display", "Controller", "Main Menu"]
        self.next_state = "MAIN_MENU"

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

    def render_text(self, index):
        color = pg.Color("red") if index == self.active_index else pg.Color("white")
        return self.default_font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0],
                  self.screen_rect.center[1] + (index * 50) + 75)
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            print("Display Test")
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
        surface.blit(self.author, (constants.SCREEN_WIDTH / 2 - self.author_rect.width / 2, 150))
        surface.blit(self.title_logo, self.title_logo_rect)
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(
                text_render, index))
