import pygame as pg

TITLE = "Intergalactic Space Blast"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 24
FPS = 60
ENEMY_MOVE_DOWN = 32
SPRITE_SHEET = './assets/images/spritesheet.png'
DEFAULT_FONT = './assets/fonts/BarcadeBrawlRegular.ttf'
DEFAULT_BACKGROUND = './assets/images/background.png'

TXT_GAME_OVER = 'Press ENTER to go to main menu, R to restart or ESC to quit'
TXT_CREDITS = 'This game was written by ...'

# user defined events
ADD_ENEMY = pg.USEREVENT + 1    # 25
DIVE_ENEMY = pg.USEREVENT + 2   # 26
ENEMY_FIRES = pg.USEREVENT + 3  # 27

ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32

'''
locations of sprites in sprite sheet
'''
# player
SS_PLAYER_X = 224
SS_PLAYER_Y = 832
SS_PLAYER_WIDTH = 99
SS_PLAYER_HEIGHT = 75
SS_PLAYER_IMAGES = 1
# enemies
SS_ENEMY1_X = 425
SS_ENEMY1_Y = 552
SS_ENEMY1_WIDTH = 93
SS_ENEMY1_HEIGHT = 84
SS_ENEMY1_IMAGES = 1
# missile
SS_MISSILE_X = 856
SS_MISSILE_Y = 421
SS_MISSILE_WIDTH = 9
SS_MISSILE_HEIGHT = 56
SS_MISSILE_IMAGES = 1
# explosion
SS_EXPLOSION_X = 80
SS_EXPLOSION_Y = 0
SS_EXPLOSION_WIDTH = 40
SS_EXPLOSION_HEIGHT = 40
SS_EXPLOSION_IMAGES = 3
