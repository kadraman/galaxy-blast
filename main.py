import sys
import pygame as pg

from states.splash_screen import SplashScreen
from states.main_menu import MainMenu
from states.game_play import GamePlay
from states.credits import Credits
from states.game_over import GameOver
from game import Game

import constants

if __name__ == "__main__":
    # setup mixer to avoid sound lag
    pg.mixer.pre_init(44100, -16, 2, 2048)
    pg.init()
    screen = pg.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    # the various states that the game can be in
    states = {
        "SPLASH_SCREEN": SplashScreen(),
        "MAIN_MENU": MainMenu(),
        "GAME_PLAY": GamePlay(),
        "GAME_OVER": GameOver(),
        "CREDITS": Credits()
    }
    # start game and set first state to "Splash Screen"
    game = Game(screen, states, "SPLASH_SCREEN")
    game.run()
    pg.quit()
    sys.exit()
