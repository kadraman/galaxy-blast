import pygame as pg

import constants
from modules.display_utils import BackGround
from sprites.base_enemy import EnemyType
from sprites.minion_enemy import MinionEnemy
from .base_state import BaseState


class MainMenu(BaseState):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.active_index = 0
        self.options = ["Start Game", "Settings", "Quit Game"]
        self.next_state = "GAME_PLAY"

        self.fancy_text_1 = None
        self.fancy_text_2 = None
        self.author = self.default_font.render(constants.AUTHOR, True, pg.Color("blue"))
        self.author_rect = self.author.get_rect(center=self.screen_rect.center)

        self.title = self.title_font.render(constants.TITLE, True, pg.Color("green"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

        self.all_sprites = pg.sprite.Group()
        self.enemy = None

    def startup(self, persistent):
        self.active_index = 0
        self.persist = persistent
        self.fancy_text_1 = self.persist["fancy_text_1"]
        self.fancy_text_2 = self.persist["fancy_text_2"]

        self.enemy = MinionEnemy(EnemyType.MINION_1, self.sprites,
                                 player_center=(300, 200),
                                 enemy_center=(300, 200),
                                 x_velocity=100, y_velocity=0,
                                 number_of_images=constants.SS_ENEMY1_IMAGES,
                                 scaled_width=constants.ENEMY1_WIDTH * 2,
                                 scaled_height=constants.ENEMY1_HEIGHT * 2)

        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.enemy)

        persistent["fancy_text_1"] = self.fancy_text_1
        persistent["fancy_text_2"] = self.fancy_text_2

        if constants.PLAY_SOUNDS:
            pg.mixer.music.load('./assets/sounds/179511__clinthammer__clinthammermusic-gamerstep-bass-triplets.wav')
            pg.mixer.music.play(-1)

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
        if self.active_index == 1:
            self.next_state = "SETTINGS"
            self.done = True
        elif self.active_index == 2:
            self.quit = True

    def get_event(self, event, controller):
        self.menu_choice(event, controller)

    def draw(self, surface):
        background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        surface.fill(self.screen_color)
        surface.blit(background.image, background.rect)

        for entity in self.all_sprites:
            surface.blit(entity.get_surface(), entity.rect)

        self.fancy_text_1.draw(self.screen, constants.AUTHOR, 320, 75)
        self.fancy_text_2.draw(self.screen, constants.TITLE, 320, 150)

        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(
                text_render, index))

    def update(self, dt):
        for entity in self.all_sprites:
            entity.update(dt)

        self.fancy_text_1.update()
        self.fancy_text_2.update()
