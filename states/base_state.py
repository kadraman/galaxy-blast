import pygame as pg

from modules.display_utils import BackGround

import constants


class BaseState(object):
    """
    Base class for game states to inherit from.
    """

    def __init__(self, persistent=None):
        if persistent is None:
            persistent = {}
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.default_screen_color = pg.Color("black")
        self.screen_color = self.default_screen_color
        self.default_background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        self.background = self.default_background
        self.font = pg.font.Font(constants.DEFAULT_FONT, constants.FONT_SIZE)
        self.author = self.font.render(constants.AUTHOR, True, pg.Color("blue"))
        self.author_rect = self.author.get_rect(center=self.screen_rect.center)
        self.title_logo = pg.image.load('./assets/images/title-text.png')
        self.title_logo_rect = self.title_logo.get_rect(center=self.screen_rect.center)
        self.done = False
        self.quit = False
        self.next_state = None
        self.previous_state = None  # not used
        self.active_index = None
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

    def get_event(self, event, controller):
        """
        Handle a single event passed by the Game object.
        """
        pass

    def update(self, dt):
        """
        Update the state. Called by the Game object once per frame.

        dt: time since last frame
        """
        pass

    def draw(self, surface):
        """
        Draw everything to the screen.
        """

    def handle_action(self):
        """
        Handle the menu item selected
        :return:
        """
        pass

    def menu_choice(self, event, controller):
        """
        Use various input devices to navigate a menu
        :param event:
        :param controller:
        """
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                if self.active_index > 0:
                    self.active_index -= 1
            elif event.key == pg.K_DOWN:
                if self.active_index < 2:
                    self.active_index += 1
            elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.handle_action()
        elif event.type == pg.JOYAXISMOTION:
            if controller.get_axis(1) >= 0.5:
                if self.active_index < 2:
                    self.active_index += 1
            if controller.get_axis(1) <= -1:
                if self.active_index > 0:
                    self.active_index -= 1
        elif event.type == pg.JOYBUTTONDOWN:
            self.handle_action()

    def weird_division(self, n, d):
        return n / d if d else 0
