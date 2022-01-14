import sys
import pygame as pg

from states.display_test import DisplayTest
from states.splash_screen import SplashScreen
from states.main_menu import MainMenu
from states.game_play import GamePlay
from states.credits import Credits
from states.game_over import GameOver
from states.settings import Settings
from states.controller_test import ControllerTest

from game import Game

import constants

if __name__ == "__main__":
    # setup mixer to avoid sound lag
    pg.mixer.pre_init(44100, -16, 2, 4096)
    pg.init()
    pg.mixer.init()
    pg.joystick.init()
    joystick = None
    try:
        joystick = pg.joystick.Joystick(0)
        joystick.init()
        print("Enabled controller: {0}".format(joystick.get_name()))
    except pg.error:
        print("no controllers found.")
    # hide the mouse cursor
    pg.mouse.set_visible(0)
    # set windows title
    pg.display.set_caption(constants.TITLE)

    screen = pg.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    # the various states that the game can be in
    states = {
        "SPLASH_SCREEN": SplashScreen(),
        "MAIN_MENU": MainMenu(),
        "GAME_PLAY": GamePlay(),
        "GAME_OVER": GameOver(),
        "CREDITS": Credits(),
        "SETTINGS": Settings(),
        "DISPLAY_TEST": DisplayTest(),
        "CONTROLLER_TEST": ControllerTest()
    }
    # start game and set first state to "Splash Screen"
    game = Game(screen, joystick, states, "SPLASH_SCREEN")
    game.run()
    pg.joystick.quit()
    pg.quit()
    sys.exit()
