import pygame as pg

AUTHOR = "kadraman's"
TITLE = "Galaxy Blast"
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FONT_SIZE = 18
FPS = 30
ENEMY_MOVE_DOWN = 16
SPRITE_SHEET = './assets/images/spritesheet.png'
DEFAULT_FONT = './assets/fonts/BarcadeBrawlRegular.ttf'
DEFAULT_BACKGROUND = './assets/images/stars.png'
MUTE_SOUND = True

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

TXT_GAME_OVER = 'Press ENTER to go to main menu, R to restart or ESC to quit'
TXT_CREDITS = 'This game was written by ...'

# user defined events
ADD_MINION_ENEMY = pg.USEREVENT + 1  # 25
ADD_MASTER_ENEMY = pg.USEREVENT + 2  # 26
DIVE_ENEMY = pg.USEREVENT + 3  # 27
LEAVE_ENEMY = pg.USEREVENT + 4  # 28
ENEMY_FIRES = pg.USEREVENT + 5  # 29

MINION_ENEMY_WIDTH = 25
MINION_ENEMY_HEIGHT = 25
MASTER_ENEMY_WIDTH = 30
MASTER_ENEMY_WIDTH = 28
BOSS_ENEMY_WIDTH = 25
BOSS_ENEMY_HEIGHT = 25

'''
locations of sprites in sprite sheet
'''
# player
SS_PLAYER_PIXEL_SIZE = 32
SS_PLAYER_X = 224
SS_PLAYER_Y = 832
SS_PLAYER_WIDTH = 99
SS_PLAYER_HEIGHT = 75
SS_PLAYER_IMAGES = 1
# enemies
SS_ENEMY1_PIXEL_SIZE = 20
SS_ENEMY1_X = 425
SS_ENEMY1_Y = 552
SS_ENEMY1_WIDTH = 93
SS_ENEMY1_HEIGHT = 84
SS_ENEMY1_IMAGES = 1
# missile
SS_MISSILE_X = 841
SS_MISSILE_Y = 647
SS_MISSILE_WIDTH = 13
SS_MISSILE_HEIGHT = 37
SS_MISSILE_IMAGES = 1
# explosion
SS_EXPLOSION_X = 80
SS_EXPLOSION_Y = 0
SS_EXPLOSION_WIDTH = 40
SS_EXPLOSION_HEIGHT = 40
SS_EXPLOSION_IMAGES = 3
# player lives
SS_PLAYER_LIVES_X = 775
SS_PLAYER_LIVES_Y = 301
SS_PLAYER_LIVES_WIDTH = 33
SS_PLAYER_LIVES_HEIGHT = 26
# score numbers
SS_DIGIT_IMAGES = 10
SS_DIGIT_WIDTH = 19
SS_DIGIT_HEIGHT = 19
SS_DIGIT0_X = 367
SS_DIGIT0_Y = 644
SS_DIGIT1_X = 205
SS_DIGIT1_Y = 688
SS_DIGIT2_X = 406
SS_DIGIT2_Y = 290
SS_DIGIT3_X = 580
SS_DIGIT3_Y = 707
SS_DIGIT4_X = 386
SS_DIGIT4_Y = 644
SS_DIGIT5_X = 628
SS_DIGIT5_Y = 646
SS_DIGIT6_X = 671
SS_DIGIT6_Y = 1002
SS_DIGIT7_X = 690
SS_DIGIT7_Y = 1004
SS_DIGIT8_X = 709
SS_DIGIT8_Y = 1004
SS_DIGIT9_X = 491
SS_DIGIT9_Y = 215
SS_DIGITX_X = 382
SS_DIGITX_Y = 814
