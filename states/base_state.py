import pygame as pg

from modules.display_utils import BackGround

import constants


class BaseState(object):
    """
    Base class for game states to inherit from.
    """

    def __init__(self, persistent={}):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.screen_color = pg.Color("black")
        self.background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        self.font = pg.font.Font(constants.DEFAULT_FONT, constants.FONT_SIZE)
        self.done = False
        self.quit = False
        self.next_state = None
        self.previous_state = None  # not used
        self.persist = persistent

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        persistent: a dict passed from state to state
        """
        self.persist = persistent

    def cleanup(self):
        """
        Called when a state finishes being active.
        Returns persistent information and resets State.done to False.
        """
        self.done = False
        return self.persist

    def get_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass

    def update(self, dt):
        """
        Update the state. Called by the Game object once  per frame.

        dt: time since last frame
        """
        pass

    def draw(self, surface):
        """
        Draw everything to the screen.
        """

    def game_choice(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                self.next_state = "MAIN_MENU"
                self.done = True
            elif event.key == pg.K_r:
                self.next_state = "GAME_PLAY"
                self.done = True
            elif event.key == pg.K_ESCAPE:
                self.quit = True
