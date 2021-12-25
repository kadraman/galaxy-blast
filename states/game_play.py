import pygame as pg
import pygame.sprite

from modules import sprite_sheet
from modules.display_utils import BackGround

from .base_state import BaseState
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.missile import Missile
from sprites.explosion import Explosion

import constants

# user defined events
ADD_ENEMY = pygame.USEREVENT + 1 # 25


class GamePlay(BaseState):
    def __init__(self):
        super(GamePlay, self).__init__()
        # send ADD_ENEMY event every 450ms
        pygame.time.set_timer(ADD_ENEMY, 450)
        self.x_velocity = 1
        self.next_state = "CREDITS"
        self.sprites = sprite_sheet.SpriteSheet(constants.SPRITE_SHEET)
        self.player = Player(self.sprites)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_enemies = pg.sprite.Group()
        self.all_bullets = pg.sprite.Group()
        self.wave_count = 0
        self.enemies = 0
        self.number_of_enemies = 10
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
        elif event.type == ADD_ENEMY:
            if self.enemies < self.number_of_enemies:
                self.add_enemy()
            elif len(self.all_enemies) == 0:
                self.enemies = 0
                self.wave_count += 1
                if self.wave_count > 2:
                    self.wave_count = 0
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
        enemy = Enemy(self.sprites, center=(self.screen_rect.right-self.enemies * 42, 40))
        self.all_enemies.add(enemy)
        self.all_sprites.add(enemy)

    def shoot_bullet(self):
        bullet = Missile(self.sprites, 0, -15)
        bullet.rect.centerx = self.player.rect.centerx
        self.all_bullets.add(bullet)
        self.all_sprites.add(bullet)
        # self.shoot_sound.play()

    def draw(self, surface):
        background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        surface.fill([255, 255, 255])
        surface.blit(background.image, background.rect)
        pressed_keys = pg.key.get_pressed()

        for entity in self.all_sprites:
            entity.update(pressed_keys)

        for entity in self.all_sprites:
            surface.blit(entity.get_surface(), entity.rect)

        for entity in self.all_enemies:
            if entity.has_landed():
                self.next_state = "GAME_OVER"
                self.done = True

        result = pg.sprite.groupcollide(self.all_enemies, self.all_bullets, True, True)
        if result:
            for key in result:
                self.score += 10
                if self.score > self.high_score:
                    self.high_score = self.score
                self.all_sprites.add(Explosion(self.sprites, key.rect.center, key.rect.size))
                # self.kill_sound.play()

        result = pg.sprite.spritecollideany(self.player, self.all_enemies)
        if result:
            self.next_state = "GAME_OVER"
            self.done = True
            self.player.kill()
