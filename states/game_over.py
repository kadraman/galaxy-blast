import pygame as pg

from modules.display_utils import BackGround

from .base_state import BaseState

import constants


class GameOver(BaseState):
    def __init__(self):
        super(GameOver, self).__init__()
        self.interval = 0
        self.music_playing = False
        self.active_index = 0
        self.options = ["Restart Game", "Main Menu", "Quit Game", ]
        self.title = self.font.render("Game Over", True, pg.Color("green"))
        title_center = (
            self.screen_rect.center[0], self.screen_rect.center[1] - 100)
        self.title_rect = self.title.get_rect(center=title_center)

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

        if constants.PLAY_SOUNDS:
            pg.mixer.music.load('./assets/sounds/339837__rocotilos__8-bit-game-over.wav')

    def update(self, dt):
        if self.interval > 50 and not self.music_playing:
            pg.mixer.music.play()
            self.music_playing = True
        else:
            self.interval += 1

    def render_text(self, index):
        color = pg.Color("red") if index == self.active_index else pg.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0],
                  self.screen_rect.center[1] + (index * 50) + 75)
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            self.next_state = "GAME_PLAY"
            self.done = True
        elif self.active_index == 1:
            self.next_state = "MAIN_MENU"
            self.done = True
        elif self.active_index == 2:
            self.quit = True

    def get_event(self, event, controller):
        self.menu_choice(event, controller)

    def draw(self, surface):
        background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        surface.fill(self.screen_color)
        surface.blit(background.image, background.rect)
        surface.blit(self.title, self.title_rect)
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(
                text_render, index))
