from random import randint

import pygame as pg
import pygame.sprite

import constants
from modules import sprite_sheet
from modules.misc_utils import safe_division
from modules.pixel_explosion import PixelExplosion
from modules.sprite_sheet import SpriteSheet
from modules.starfield import StarField
from sprites.base_enemy import EnemyType
from sprites.boss_enemy import BossEnemy
from sprites.explosion import Explosion
from sprites.master_enemy import MasterEnemy
from sprites.mine import Mine
from sprites.minion_enemy import MinionEnemy
from sprites.missile import Missile
from sprites.player import Player
from .base_state import BaseState


class GamePlay(BaseState):
    def __init__(self):
        super(GamePlay, self).__init__()

        # send ADD_MINION_ENEMY event every 450ms
        pygame.time.set_timer(constants.ADD_MINION_ENEMY, 450)
        # send ADD_MASTER_ENEMY event every 12000ms
        pygame.time.set_timer(constants.ADD_MASTER_ENEMY, 12000)
        # send ADD_BOSS_ENEMY event every 18000ms
        pygame.time.set_timer(constants.ADD_BOSS_ENEMY, 18000)
        # send DIVE_ENEMY event every 6000ms
        pygame.time.set_timer(constants.DIVE_ENEMY, 6000)
        # send ENEMY_FIRES event every 1000ms
        pygame.time.set_timer(constants.ENEMY_FIRES, 1000)

        self.pixel_explosion = None
        self.starfield = StarField()
        self.shoot_sound = pg.mixer.Sound("./assets/sounds/321102__nsstudios__laser1.ogg")
        self.kill_sound = pg.mixer.Sound("./assets/sounds/170145__timgormly__8-bit-explosion1.ogg")
        self.hit_sound = pg.mixer.Sound("./assets/sounds/344303__musiclegends__explosion52.ogg")
        self.level_up_sound = pg.mixer.Sound("./assets/sounds/448266__henryrichard__sfx-clear.ogg")
        self.game_over_explosion = pg.mixer.Sound("./assets/sounds/368591__jofae__retro-explosion.ogg")

        self.score_font = pg.font.Font(constants.DEFAULT_FONT, constants.SCORE_FONT_SIZE)

        self.x_velocity = 1
        self.next_state = "MAIN_MENU"
        self.player_velocity = 100  # original player velocity
        self.sprites = sprite_sheet.SpriteSheet(constants.SPRITE_SHEET)
        self.player = Player(self.sprites, self.player_velocity, constants.PLAYER_WIDTH, constants.PLAYER_HEIGHT)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_enemies = pg.sprite.Group()
        self.enemy_missiles = pg.sprite.Group()
        self.enemy_mines = pg.sprite.Group()
        self.player_missiles = pg.sprite.Group()
        self.life_image = self.sprites.image_at(pg.Rect(constants.SS_PLAYER_LIVES_X, constants.SS_PLAYER_LIVES_Y,
                                                        constants.SS_PLAYER_WIDTH, constants.SS_PLAYER_HEIGHT))

        self.wave_count = 0
        self.minion_1_enemies = 0
        self.minion_2_enemies = 0
        self.minion_3_enemies = 0
        self.minion_1_y_velocity = 50
        self.minion_2_y_velocity = 50
        self.minion_3_y_velocity = 50
        self.max_minion_1_enemies = 12
        self.max_minion_2_enemies = 10
        self.max_minion_3_enemies = 8
        self.attacking_minion_enemies = 0
        self.max_attacking_minion_enemies = 3
        self.minion_1_y_start = 40
        self.minion_2_y_start = 75
        self.minion_3_y_start = 110
        self.master_enemies = 0
        self.attacking_master_enemies = 0
        self.max_attacking_master_enemies = 1
        self.boss_enemies = 0
        self.attacking_boss_enemies = 0
        self.max_attacking_boss_enemies = 1
        self.player_missile_velocity = -250
        self.enemy_missile_velocity = 100
        self.lives = 3
        self.score = 0
        self.high_score = 0
        self.freeze = False
        self.interval = 0

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

        persistent['score'] = self.score
        persistent['high_score'] = self.high_score

        self.player = Player(self.sprites, self.player_velocity, constants.PLAYER_WIDTH, constants.PLAYER_HEIGHT)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.player_missiles = pg.sprite.Group()
        self.all_enemies = pg.sprite.Group()
        self.enemy_missiles = pygame.sprite.Group()

        self.done = False
        self.wave_count = 0
        self.minion_1_enemies = 0
        self.minion_2_enemies = 0
        self.minion_3_enemies = 0
        self.minion_1_y_velocity = 0
        self.minion_2_y_velocity = 50
        self.minion_3_y_velocity = 50
        self.max_minion_1_enemies = 12
        self.max_minion_2_enemies = 10
        self.max_minion_3_enemies = 8
        self.attacking_minion_enemies = 0
        self.max_attacking_minion_enemies = 3
        self.player_missile_velocity = -250
        self.enemy_missile_velocity = 125
        self.lives = 3
        self.score = 0
        self.freeze = False
        self.interval = 0

        if constants.PLAY_SOUNDS:
            pg.mixer.music.load('./assets/sounds/251461__joshuaempyre__arcade-music-loop.wav')
            pg.mixer.music.play(-1)

    def cleanup(self):
        self.persist['score'] = self.score
        self.persist['high_score'] = self.high_score

    def get_event(self, event, controller):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == constants.ADD_MINION_ENEMY:
            if self.minion_1_enemies < self.max_minion_1_enemies:
                self.add_enemy(EnemyType.MINION_1)
            elif self.minion_2_enemies < self.max_minion_2_enemies:
                self.add_enemy(EnemyType.MINION_2)
            elif self.minion_3_enemies < self.max_minion_3_enemies:
                self.add_enemy(EnemyType.MINION_3)
            elif len(self.all_enemies) == 0:
                self.next_wave()
        elif event.type == constants.ADD_MASTER_ENEMY:
            if self.master_enemies == 0:
                self.add_enemy(EnemyType.MASTER)
        elif event.type == constants.ADD_BOSS_ENEMY:
            if self.boss_enemies == 0:
                self.add_enemy(EnemyType.BOSS)
        elif event.type == constants.DIVE_ENEMY:
            self.enemy_attack()
        elif event.type == constants.ENEMY_FIRES:
            self.enemy_fires()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.player.is_moving_left = True
            elif event.key == pg.K_RIGHT:
                self.player.is_moving_right = True
            elif event.key == pg.K_UP:
                self.player.is_moving_up = True
            elif event.key == pg.K_DOWN:
                self.player.is_moving_down = True
        elif event.type == pg.KEYUP:
            # TODO: Pause rather than return to main menu
            if event.key == pg.K_ESCAPE:
                self.next_state = "MAIN_MENU"
                self.done = True
            elif event.key == pg.K_LEFT:
                self.player.is_moving_left = False
            elif event.key == pg.K_RIGHT:
                self.player.is_moving_right = False
            elif event.key == pg.K_UP:
                self.player.is_moving_up = False
            elif event.key == pg.K_DOWN:
                self.player.is_moving_down = False
            elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                if len(self.player_missiles) < constants.MAX_PLAYER_MISSILES:
                    self.player_fires()
        elif event.type == pg.JOYAXISMOTION:
            if controller.get_axis(0) >= 0.5:
                self.player.is_moving_right = True
            else:
                self.player.is_moving_right = False
            if controller.get_axis(0) <= -1:
                self.player.is_moving_left = True
            else:
                self.player.is_moving_left = False
            if controller.get_axis(1) >= 0.5:
                self.player.is_moving_down = True
            else:
                self.player.is_moving_down = False
            if controller.get_axis(1) <= -1:
                self.player.is_moving_up = True
            else:
                self.player.is_moving_down = False
        elif event.type == pg.JOYBUTTONUP:
            if len(self.player_missiles) < 2:
                self.player_fires()

    def draw(self, surface):
        surface.fill(self.screen_color)
        self.starfield.render(surface)

        self.draw_scores_and_lives(surface)

        for entity in self.all_sprites:
            surface.blit(entity.get_surface(), entity.rect)

        if self.pixel_explosion is not None:
            self.pixel_explosion.render(surface)

    def update(self, dt):
        self.master_enemies = self.boss_enemies = 0
        for entity in self.all_enemies:
            if entity.enemy_type == EnemyType.MASTER:
                self.master_enemies = 1
            elif entity.enemy_type == EnemyType.BOSS:
                self.boss_enemies = 1

        for entity in self.all_sprites:
            entity.update(dt)

        if self.pixel_explosion is not None:
            self.pixel_explosion.update(dt)

        # we are done just wait for animations to complete
        if self.freeze:
            if self.interval >= 20:
                self.done = True
            else:
                self.interval += 1
        else:
            result = pg.sprite.groupcollide(self.all_enemies, self.player_missiles, False, True)
            if result:
                for key in result:
                    kill_enemy = False
                    if key.enemy_type == EnemyType.BOSS:
                        if key.hits >= key.max_hits-1:
                            self.boss_enemies = 0
                            kill_enemy = True
                        else:
                            if constants.PLAY_SOUNDS:
                                self.kill_sound.play()
                            self.all_sprites.add(Explosion(self.sprites, key.rect.center, key.rect.size))
                            key.hits += 1
                    elif key.enemy_type == EnemyType.MASTER:
                        self.master_enemies = 0
                        kill_enemy = True
                    else:
                        kill_enemy = True
                    if kill_enemy:
                        key.kill()
                        self.all_sprites.add(Explosion(self.sprites, key.rect.center, key.rect.size))
                        self.score += key.points
                        if constants.PLAY_SOUNDS:
                            self.kill_sound.play()
                    if self.score > self.high_score:
                        self.high_score = self.score

            result = pygame.sprite.spritecollide(self.player, self.enemy_missiles, True)
            if result:
                self.all_sprites.add(Explosion(self.sprites, self.player.rect.center, self.player.rect.size))
                if self.lives == 1:
                    self.game_over()
                else:
                    if constants.PLAY_SOUNDS:
                        self.hit_sound.play()
                    self.pixel_explosion = PixelExplosion(self.player.rect.centerx, self.player.rect.centery, 300)
                    self.lives -= 1

            result = pg.sprite.spritecollideany(self.player, self.all_enemies)
            if result:
                if self.lives == 1:
                    self.game_over()
                else:
                    self.lives -= 1

            mine = pg.sprite.spritecollideany(self.player, self.enemy_mines)
            if mine:
                if self.lives == 1:
                    self.game_over()
                else:
                    if constants.PLAY_SOUNDS:
                        self.hit_sound.play()
                    mine.kill()
                    self.pixel_explosion = PixelExplosion(self.player.rect.centerx, self.player.rect.centery, 300)
                    self.lives -= 1

    '''
    Supporting functions
    '''

    def add_enemy(self, enemy_type):
        if enemy_type == EnemyType.MINION_1:
            enemy = MinionEnemy(enemy_type, self.sprites, self.player.rect,
                                enemy_center=(
                                    self.screen_rect.left + 50 + (self.minion_1_enemies * 50), self.minion_1_y_start),
                                x_velocity=100, y_velocity=self.minion_1_y_velocity,
                                number_of_images=constants.SS_ENEMY1_IMAGES,
                                scaled_width=constants.ENEMY1_WIDTH, scaled_height=constants.ENEMY2_HEIGHT)
            self.minion_1_enemies += 1
        elif enemy_type == EnemyType.MINION_2:
            enemy = MinionEnemy(enemy_type, self.sprites, self.player.rect,
                                enemy_center=(
                                    self.screen_rect.left + 80 + (self.minion_2_enemies * 50), self.minion_2_y_start),
                                x_velocity=100, y_velocity=self.minion_2_y_velocity,
                                number_of_images=constants.SS_ENEMY2_IMAGES,
                                scaled_width=constants.ENEMY2_WIDTH, scaled_height=constants.ENEMY2_HEIGHT)
            self.minion_2_enemies += 1
        elif enemy_type == EnemyType.MINION_3:
            enemy = MinionEnemy(enemy_type, self.sprites, self.player.rect,
                                enemy_center=(
                                    self.screen_rect.left + 110 + (self.minion_3_enemies * 50), self.minion_3_y_start),
                                x_velocity=100, y_velocity=self.minion_3_y_velocity,
                                number_of_images=constants.SS_ENEMY3_IMAGES,
                                scaled_width=constants.ENEMY3_WIDTH, scaled_height=constants.ENEMY3_HEIGHT)
            self.minion_3_enemies += 1
        elif enemy_type == EnemyType.MASTER:
            y_start = randint(140, constants.SCREEN_HEIGHT - 100)
            # start on right or left side of screen
            x_start = 0
            x_velocity = 100
            if randint(1, 2) == 1:
                x_start = constants.SCREEN_WIDTH
                x_velocity = -100
            enemy = MasterEnemy(enemy_type, self.sprites, self.player.rect,
                                center=(x_start, y_start),
                                x_velocity=x_velocity, y_velocity=0,
                                number_of_images=constants.SS_MASTER_ENEMY_IMAGES,
                                scaled_width=constants.MASTER_ENEMY_WIDTH, scaled_height=constants.MASTER_ENEMY_HEIGHT)
            self.master_enemies += 1
        elif enemy_type == EnemyType.BOSS:
            y_start = 180
            x_start = 320
            x_velocity = 200
            enemy = BossEnemy(enemy_type, self.sprites, self.player.rect,
                              center=(x_start, y_start),
                              x_velocity=x_velocity, y_velocity=0,
                              number_of_images=constants.SS_BOSS_ENEMY_IMAGES,
                              scaled_width=constants.BOSS_ENEMY_WIDTH, scaled_height=constants.BOSS_ENEMY_HEIGHT)
            self.boss_enemies += 1

        self.all_enemies.add(enemy)
        self.all_sprites.add(enemy)

    def player_fires(self):
        x_velocity = 0
        y_velocity = self.player_missile_velocity
        missile = Missile(self.sprites, x_velocity, y_velocity, True, False)
        missile.rect.centerx = self.player.rect.centerx
        missile.rect.centery = self.player.rect.centery
        self.player_missiles.add(missile)
        self.all_sprites.add(missile)
        if constants.PLAY_SOUNDS:
            self.shoot_sound.play()

    def enemy_attack(self):
        if self.attacking_minion_enemies < self.max_attacking_minion_enemies:
            for entity in self.all_enemies:
                if not entity.is_attacking() and entity.enemy_type != EnemyType.MASTER \
                        and entity.enemy_type != EnemyType.BOSS \
                        and entity.enemy_type != EnemyType.MINION_1 and randint(0, 2) < 1:
                    entity.attack()

    def enemy_fires(self):
        num_enemies = len(self.all_enemies)
        if num_enemies > 0:
            enemy_index = randint(0, num_enemies - 1)
            start_missile = None
            start_mine = None
            start_beam = None
            for index, enemy in enumerate(self.all_enemies):
                # don't fire if master enemy as they lay mines
                if enemy.enemy_type == EnemyType.MASTER and randint(1, 10) > 5:
                    start_mine = enemy.rect.center
                elif enemy.enemy_type == EnemyType.BOSS and randint(1, 3) == 2:
                    start_beam = enemy.rect.center
                elif enemy.enemy_type == EnemyType.MINION_1 and index == enemy_index:
                    start_missile = enemy.rect.center
                elif enemy.enemy_type == EnemyType.MINION_2 and index == enemy_index:
                    start_missile = enemy.rect.center
                elif enemy.enemy_type == EnemyType.MINION_3 and index == enemy_index:
                    start_missile = enemy.rect.center

            if start_missile and start_missile[1] < constants.SCREEN_HEIGHT:
                y_velocity = self.enemy_missile_velocity
                dx = self.player.rect.centerx - start_missile[0]
                dy = self.player.rect.centery - start_missile[1]

                number_of_steps = safe_division(dy, y_velocity)
                x_velocity = safe_division(dx, number_of_steps)

                missile = Missile(self.sprites, x_velocity, y_velocity, False, False)
                missile.rect.centerx = start_missile[0]
                missile.rect.centery = start_missile[1]

                self.enemy_missiles.add(missile)
                self.all_sprites.add(missile)

            if start_mine and 50 < start_mine[0] < constants.SCREEN_WIDTH - 50:
                if constants.SCREEN_HEIGHT - 50 > start_mine[1] > 50:
                    mine = Mine(self.sprites, 0, 0, constants.MINE_WIDTH, constants.MINE_HEIGHT)
                    mine.rect.centerx = start_mine[0]
                    mine.rect.centery = start_mine[1]

                    self.enemy_mines.add(mine)
                    self.all_sprites.add(mine)

            if start_beam:
                for i in range(3):
                    y_velocity = 250

                    missile = Missile(self.sprites, 0, y_velocity, False, True)
                    missile.rect.centerx = start_beam[0]
                    missile.rect.centery = start_beam[1] + (20 * i)

                    self.enemy_missiles.add(missile)
                    self.all_sprites.add(missile)

    def draw_scores_and_lives(self, surface):
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

    def next_wave(self):
        if constants.PLAY_SOUNDS:
            self.level_up_sound.play()
        self.score += 50
        self.minion_1_enemies = 0
        self.minion_2_enemies = 0
        self.minion_3_enemies = 0
        self.master_enemies = 0
        self.boss_enemies = 0
        self.wave_count += 1
        self.minion_1_y_velocity += 0  # does not dive
        self.minion_2_y_velocity += 5
        self.minion_3_y_velocity += 5
        if self.max_attacking_minion_enemies != (self.max_minion_2_enemies + self.max_minion_3_enemies):
            self.max_attacking_minion_enemies += 1

    def game_over(self):
        pg.mixer.music.stop()

        self.next_state = "GAME_OVER"
        self.freeze = True
        self.pixel_explosion = PixelExplosion(self.player.rect.centerx, self.player.rect.centery, 500)
        if constants.PLAY_SOUNDS:
            self.game_over_explosion.play()
        self.player.kill()
