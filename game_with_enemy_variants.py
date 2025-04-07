# core/game.py

import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from core.asset_loader import AssetLoader
from core.level_manager import LevelManager
from core.event_handler import EventHandler
from core.enemy_manager import EnemyManager

from entities.player import Player
from entities.bullet import Bullet
from entities.enemy_bullet import EnemyBullet
from entities.explosion import Explosion

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invader - Enemy Variants")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "playing"

        self.asset_loader = AssetLoader()
        self.level_manager = LevelManager(self.asset_loader)
        self.event_handler = EventHandler(self)

        # Sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        # Load enemy variant images
        self.enemy_images = {
            'basic': self.asset_loader.load_image('enemy_basic', 'enemy.png', scale=(40, 40)),
            'fast': self.asset_loader.load_image('enemy_fast', 'enemy_fast.png', scale=(36, 36)),
            'tanky': self.asset_loader.load_image('enemy_tanky', 'enemy_tank.png', scale=(50, 50)),
        }

        # Player setup
        player_img = self.asset_loader.load_image("player", "player.png", scale=(30, 30))
        bullet_img = self.asset_loader.load_image("bullet", "player-bullet.png", scale=(10, 20))
        self.enemy_bullet_img = self.asset_loader.load_image("enemy_bullet", "enemy-bullet.png", scale=(10, 20))
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, player_img, bullet_img)
        self.player_group.add(self.player)

        # Explosion
        self.explosion_img = self.asset_loader.load_image("explosion", "explosion.png", scale=(40, 40))

        # Sounds
        self.sound_shoot = self.asset_loader.load_sound("shoot", "shoot.wav")
        self.sound_explosion = self.asset_loader.load_sound("explosion", "explosion.wav")
        self.sound_game_over = self.asset_loader.load_sound("game_over", "game_over.wav")
        self.sound_enemy_shoot = self.asset_loader.load_sound("enemy_shoot", "enemy_shoot.wav")
        self.sound_victory = self.asset_loader.load_sound("victory", "victory.ogg")

        # Music
        pygame.mixer.music.load("assets/sounds/music.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # HUD
        self.font = pygame.font.SysFont("Arial", 20)
        self.score = 0
        self.lives = 3
        self.heart_img = self.asset_loader.load_image("heart", "heart.png", scale=(30, 30))
        self.heart_size = (30, 30)

        # Enemy manager
        self.enemy_manager = EnemyManager(self.enemy_group, self.level_manager.enemy_speed)
        self.level_manager.spawn_enemies(self.enemy_group, self.enemy_images)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.event_handler.handle()

            if self.state == "playing":
                self.update()
                self.draw()
            elif self.state == "paused":
                self.draw_paused()
            elif self.state == "game_over":
                self.draw_game_over()

    # Remaining methods (update, draw, etc.) assumed present...