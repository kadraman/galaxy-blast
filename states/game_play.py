import pygame as pg
import pygame.sprite

from random import seed
from random import randint

from modules import sprite_sheet
from modules.display_utils import BackGround
from modules.sound_utils import SoundEffect
from modules.starfield import StarField
from modules.sprite_sheet import SpriteSheet

from .base_state import BaseState
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.missile import Missile
from sprites.digit import Digit
from sprites.explosion import Explosion

import constants


class GamePlay(BaseState):
    def __init__(self):
        super(GamePlay, self).__init__()
        # send ADD_ENEMY event every 450ms
        pygame.time.set_timer(constants.ADD_ENEMY, 450)
        # send DIVE_ENEMY event every 6000ms
        pygame.time.set_timer(constants.DIVE_ENEMY, 6000)
        # send ENEMY_FIRES event every 1000ms
        pygame.time.set_timer(constants.ENEMY_FIRES, 1000)

        self.starfield = StarField()
        self.laser = SoundEffect("assets/sounds/laser.ogg")
        self.shoot_sound = pg.mixer.Sound("./assets/sounds/laser.ogg")
        self.kill_sound = pg.mixer.Sound("./assets/sounds/kill.ogg")
        self.hit_sound = pg.mixer.Sound("./assets/sounds/explosion.ogg")

        self.score_font = pg.font.Font(constants.DEFAULT_FONT, 12)

        self.x_velocity = 1
        self.next_state = "CREDITS"
        self.sprites = sprite_sheet.SpriteSheet(constants.SPRITE_SHEET)
        self.player = Player(self.sprites)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_enemies = pg.sprite.Group()
        self.enemy_missiles = pygame.sprite.Group()
        self.all_bullets = pg.sprite.Group()

        life_sprite = SpriteSheet('./assets/images/player-1.png')
        self.life_image = life_sprite.image_at(pg.Rect(0, 0, 16, 16))
        self.digit = Digit(self.sprites)

        self.padding_top = 32
        self.enemy_diving = False
        self.wave_count = 0
        self.enemies = 0
        self.number_of_enemies = 10
        self.number_of_attacking_enemies = 0
        self.max_attacking_enemies = 3
        self.lives = 3
        self.score = 0
        self.high_score = 0

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

        self.player = Player(self.sprites)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_bullets = pg.sprite.Group()
        self.all_enemies = pg.sprite.Group()
        self.enemy_missiles = pygame.sprite.Group()

        self.done = False
        self.enemy_diving = False
        self.wave_count = 0
        self.enemies = 0
        self.number_of_enemies = 10
        self.number_of_attacking_enemies = 0
        self.max_attacking_enemies = 3
        self.lives = 3
        self.score = 0

    def get_event(self, event, joystick):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == constants.ADD_ENEMY:
            if self.enemies < self.number_of_enemies:
                self.add_enemy()
            elif len(self.all_enemies) == 0:
                self.enemies = 0
                self.wave_count += 1
                if self.wave_count > 2:
                    self.wave_count = 0
        elif event.type == constants.DIVE_ENEMY:
            self.enemy_attack()
        elif event.type == constants.ENEMY_FIRES:
            self.enemy_fires()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.player.is_moving_left = True
            elif event.key == pg.K_RIGHT:
                self.player.is_moving_right = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.done = True
            elif event.key == pg.K_LEFT:
                self.player.is_moving_left = False
            elif event.key == pg.K_RIGHT:
                self.player.is_moving_right = False
            elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                if len(self.all_bullets) < 2:
                    self.player_fires()
        elif event.type == pg.JOYAXISMOTION:
            if joystick.get_axis(0) >= 0.5:
                self.player.is_moving_right = True
            else:
                self.player.is_moving_right = False
            if joystick.get_axis(0) <= -1:
                self.player.is_moving_left = True
            else:
                self.player.is_moving_left = False
        elif event.type == pg.JOYBUTTONUP:
            if len(self.all_bullets) < 2:
                self.player_fires()

    def draw(self, surface):
        # background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        # surface.fill([255, 255, 255])
        # surface.blit(background.image, background.rect)
        surface.fill(self.screen_color)
        self.starfield.render(surface)

        # Display score and lives
        self.draw_score(surface)
        '''
        score = str(self.score)
        for i in range(1, len(score) + 1):
            # In Python, a negative index into a list (or in this case, into a string) gives you items in reverse order,
            # e.g. 'hello'[-1] gives 'o', 'hello'[-2] gives 'l', etc.
            digit = int(score[-i])
            surface.blit(self.digit.get_surface(digit), (468 - i * 24, 5))
        '''

        for entity in self.all_sprites:
            surface.blit(entity.get_surface(), entity.rect)

    def update(self, dt):
        for entity in self.all_sprites:
            entity.update(dt)

        result = pg.sprite.groupcollide(self.all_enemies, self.all_bullets, True, True)
        if result:
            for key in result:
                self.score += 10
                if self.score > self.high_score:
                    self.high_score = self.score
                self.all_sprites.add(Explosion(self.sprites, key.rect.center, key.rect.size))
                if not constants.MUTE_SOUND:
                    self.kill_sound.play()

        result = pygame.sprite.spritecollide(self.player, self.enemy_missiles, True)
        if result:
            self.all_sprites.add(Explosion(self.sprites, self.player.rect.center, self.player.rect.size))
            # self.all_sprites.add(Explosion(self.sprites, result.rect[0], result.rect[1]))
            # self.all_sprites.add(Explosion(self.sprites, result.rect[0] - 30, result.rect[1] - 30))
            # self.all_sprites.add(Explosion(self.sprites, result.rect[0] + 30, result.rect[1] + 30))
            # self.all_sprites.add(Explosion(self.sprites, result.rect[0], result.rect[1] - 30))
            if not constants.MUTE_SOUND:
                self.hit_sound.play()
            # self.freeze = True
            if self.lives == 1:
                self.next_state = "GAME_OVER"
                self.done = True
                self.player.kill()
            else:
                self.lives -= 1

        result = pg.sprite.spritecollideany(self.player, self.all_enemies)
        if result:
            if self.lives == 1:
                self.next_state = "GAME_OVER"
                self.done = True
                self.player.kill()
            else:
                self.lives -= 1

    '''
    Supporting functions
    '''

    def add_enemy(self):
        self.enemies += 1
        enemy = Enemy(self.sprites, center=(self.screen_rect.left + 50 + (self.enemies * 50), self.padding_top))
        self.all_enemies.add(enemy)
        self.all_sprites.add(enemy)

    def player_fires(self):
        x_velocity = 0
        y_velocity = -250
        bullet = Missile(self.sprites, x_velocity, y_velocity)
        bullet.rect.centerx = self.player.rect.centerx
        self.all_bullets.add(bullet)
        self.all_sprites.add(bullet)
        if not constants.MUTE_SOUND:
            self.shoot_sound.play()

    def enemy_attack(self):
        if self.number_of_attacking_enemies < self.max_attacking_enemies:
            for entity in self.all_enemies:
                if not entity.is_attacking() and randint(0, 2) < 1:
                    entity.attack()

    def enemy_fires(self):
        num_enemies = len(self.all_enemies)
        if num_enemies > 0:
            enemy_index = randint(0, num_enemies - 1)
            start_missile = None
            for index, enemy in enumerate(self.all_enemies):
                if index == enemy_index:
                    start_missile = enemy.rect.center

            if start_missile[1] < 400:
                y_velocity = 100
                dx = self.player.rect.centerx - start_missile[0]
                dy = self.player.rect.centery - start_missile[1]

                number_of_steps = self.weird_division(dy, y_velocity)
                x_velocity = self.weird_division(dx, number_of_steps)

                missile = Missile(self.sprites, x_velocity, y_velocity)
                missile.rect.centerx = start_missile[0]
                missile.rect.centery = start_missile[1]

                self.enemy_missiles.add(missile)
                self.all_sprites.add(missile)

    def draw_score(self, surface):
        score = self.score_font.render('SCORE', True, (255, 20, 20))
        surface.blit(score, (constants.SCREEN_WIDTH / 2 - 280 - score.get_rect().width / 2, 2))
        score = self.score_font.render(str(self.score), True, (255, 255, 255))
        surface.blit(score, (constants.SCREEN_WIDTH / 2 - 280 - score.get_rect().width / 2, 20))

        high_score = self.score_font.render('HIGH SCORE', True, (255, 20, 20))
        surface.blit(high_score, (constants.SCREEN_WIDTH / 2 - high_score.get_rect().width / 2, 2))
        high_score = self.score_font.render(str(self.high_score), True, (255, 255, 255))
        surface.blit(high_score, (constants.SCREEN_WIDTH / 2 - high_score.get_rect().width / 2, 20))

        lives = self.score_font.render('LIVES', True, (255, 20, 20))
        surface.blit(lives, (constants.SCREEN_WIDTH - lives.get_rect().width - 5, 2))

        for i in range(self.lives):
            surface.blit(self.life_image, (constants.SCREEN_WIDTH - (i * 32 + 16), 20))
