import pygame as pg

from .base_state import BaseState

from modules.display_utils import BackGround

import constants


class MainMenu(BaseState):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.active_index = 0
        self.options = ["Start Game", "Quit Game"]
        self.next_state = "GAME_PLAY"

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

    def render_text(self, index):
        color = pg.Color("red") if index == self.active_index else pg.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0],
                  self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            self.done = True
        elif self.active_index == 1:
            self.quit = True

    def get_event(self, event, joystick):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                self.active_index = 1 if self.active_index <= 0 else 0
            elif event.key == pg.K_DOWN:
                self.active_index = 0 if self.active_index >= 1 else 1
            elif event.key == pg.K_RETURN:
                self.handle_action()
        elif event.type == pg.JOYAXISMOTION:
            if joystick.get_axis(0) >= 0.5:
                print("right has been pressed")
            if joystick.get_axis(0) <= -1:
                print("left has been pressed")
            if joystick.get_axis(1) >= 0.5:
                print("Down has been pressed")
                self.active_index = 0 if self.active_index >= 1 else 1
            if joystick.get_axis(1) <= -1:
                print("Up has been pressed")
                self.active_index = 1 if self.active_index <= 0 else 0
        elif event.type == pg.JOYBUTTONDOWN:
            print("Joystick Button pressed")

    def draw(self, surface):
        background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        surface.fill([255, 255, 255])
        surface.blit(background.image, background.rect)
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(
                text_render, index))
