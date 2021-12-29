import pygame as pg
import pygame.sprite

from random import seed
from random import randint

from modules import sprite_sheet
from modules.display_utils import BackGround

from .base_state import BaseState
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.missile import Missile
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

        self.x_velocity = 1
        self.next_state = "CREDITS"
        self.sprites = sprite_sheet.SpriteSheet(constants.SPRITE_SHEET)
        self.player = Player(self.sprites)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_enemies = pg.sprite.Group()
        self.enemy_missiles = pygame.sprite.Group()
        self.all_bullets = pg.sprite.Group()
        self.enemy_diving = False
        self.wave_count = 0
        self.enemies = 0
        self.number_of_enemies = 10
        self.number_of_attacking_enemies = 0
        self.max_attacking_enemies = 3
        self.score = 0
        self.high_score = 0

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = pg.Color(color)
        self.player = Player(self.sprites)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_bullets = pg.sprite.Group()
        self.all_enemies = pg.sprite.Group()

    def get_event(self, event):
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
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.done = True
            elif event.key == pg.K_SPACE:
                if len(self.all_bullets) < 2:
                    self.shoot_bullet()

    def update(self, dt):
        pass

    def add_enemy(self):
        self.enemies += 1
        enemy = Enemy(self.sprites, center=(self.screen_rect.left+50+(self.enemies * 50), 25))
        self.all_enemies.add(enemy)
        self.all_sprites.add(enemy)

    def shoot_bullet(self):
        bullet = Missile(self.sprites, 0, -15)
        bullet.rect.centerx = self.player.rect.centerx
        self.all_bullets.add(bullet)
        self.all_sprites.add(bullet)
        # self.shoot_sound.play()

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
                ySpeed = 7
                dx = self.player.rect.centerx - start_missile[0]
                dy = self.player.rect.centery - start_missile[1]

                number_of_steps = dy / ySpeed
                xSpeed = dx / number_of_steps

                missile = Missile(self.sprites, xSpeed, ySpeed)
                missile.rect.centerx = start_missile[0]
                missile.rect.centery = start_missile[1]

                self.enemy_missiles.add(missile)
                self.all_sprites.add(missile)

    def draw(self, surface):
        background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        surface.fill([255, 255, 255])
        surface.blit(background.image, background.rect)
        pressed_keys = pg.key.get_pressed()

        for entity in self.all_sprites:
            entity.update(pressed_keys)

        for entity in self.all_sprites:
            surface.blit(entity.get_surface(), entity.rect)

        result = pg.sprite.groupcollide(self.all_enemies, self.all_bullets, True, True)
        if result:
            print("Shot an enemy")
            for key in result:
                self.score += 10
                if self.score > self.high_score:
                    self.high_score = self.score
                self.all_sprites.add(Explosion(self.sprites, key.rect.center, key.rect.size))
                # self.kill_sound.play()

        result = pygame.sprite.spritecollideany(self.player, self.enemy_missiles)
        if result:
            print("Shot by an enemy")
            self.all_sprites.add(Explosion(self.sprites, self.player.rect.center, self.player.rect.size))
            # self.all_sprites.add(Explosion(self.explosion_sprites, result.rect[0], result.rect[1]))
            # self.all_sprites.add(Explosion(self.explosion_sprites, result.rect[0] - 30, result.rect[1] - 30))
            # self.all_sprites.add(Explosion(self.explosion_sprites, result.rect[0] + 30, result.rect[1] + 30))
            # self.all_sprites.add(Explosion(self.explosion_sprites, result.rect[0], result.rect[1] - 30))
            # self.kill_sound.play()
            # self.freeze = True
            self.next_state = "GAME_OVER"
            self.done = True
            self.player.kill()

        result = pg.sprite.spritecollideany(self.player, self.all_enemies)
        if result:
            print("Enemy collided with player")
            self.next_state = "GAME_OVER"
            self.done = True
            self.player.kill()
