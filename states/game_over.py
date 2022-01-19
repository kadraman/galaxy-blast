import pygame as pg

import constants
from modules.display_utils import BackGround, FancyText
from .base_state import BaseState


class GameOver(BaseState):
    def __init__(self):
        super(GameOver, self).__init__()
        self.interval = 0
        self.music_playing = False
        self.active_index = 0
        self.options = ["Restart Game", "Main Menu", "Quit Game", ]
        self.score = 0
        self.score_str = ""
        self.high_score = 0
        self.high_score_str = ""

        self.game_over_text = FancyText(constants.DEFAULT_FONT, constants.GAME_OVER_FONT_SIZE, [20, 150, 20])
        self.game_over_text.color_direction = [0, 0, 1]
        self.game_over_text.color_speed = 5

        self.score_text = FancyText(constants.DEFAULT_FONT, constants.DEFAULT_FONT_SIZE, [20, 150, 20])
        self.score_text.color_direction = [0, 0, 1]
        self.score_text.color_speed = 5

        self.high_score_text = FancyText(constants.DEFAULT_FONT, 20, [50, 150, 20])
        self.high_score_text.color_direction = [1, -1, 1]
        self.high_score_text.color_speed = 5

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
        self.score = self.persist["score"]
        self.score_str = "Score: " + str(self.score)
        self.high_score = self.persist["high_score"]
        if self.score >= self.high_score:
            self.high_score_str = "A new high score"

        if constants.PLAY_SOUNDS:
            pg.mixer.music.load('./assets/sounds/339837__rocotilos__8-bit-game-over.wav')

    def update(self, dt):
        if constants.PLAY_SOUNDS and self.interval > 50 and not self.music_playing:
            pg.mixer.music.play()
            self.music_playing = True
        else:
            self.interval += 1

    def render_text(self, index):
        color = pg.Color("red") if index == self.active_index else pg.Color("white")
        return self.default_font.render(self.options[index], True, color)

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

        self.game_over_text.draw(self.screen, constants.GAME_OVER, 320, 75)
        self.score_text.draw(self.screen, self.score_str, 320, 150)
        if self.score >= self.high_score:
            self.high_score_text.draw(self.screen, self.high_score_str, 320, 200)

        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(
                text_render, index))

    def update(self, dt):
        self.game_over_text.update()
        if self.score >= self.high_score:
            self.high_score_text.update()
