# core/game.py
import pygame
import pygame.mixer
import core.settings as settings
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
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Modular Space Invader")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "playing"  # Possible: "playing", "paused", "game_over"

        # Modules
        self.asset_loader = AssetLoader()
        self.level_manager = LevelManager(self.asset_loader)
        self.event_handler = EventHandler(self)

        # Init background music
        pygame.mixer.music.load("assets/sounds/background-music.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop the music indefinitely

        # Init sound
        self.sound_shoot = self.asset_loader.load_sound("shoot", "player-bullet-sound.mp3")
        self.sound_explosion = self.asset_loader.load_sound("explosion", "enemy-explosion.mp3")
        self.sound_enemy_shoot = self.asset_loader.load_sound("enemy_shoot", "enemy-bullet-sound.mp3")
        self.sound_game_over = self.asset_loader.load_sound("game_over", "game-over.mp3")
        self.sound_victory = self.asset_loader.load_sound("victory", "victory-music.ogg")

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

        # Entities
        player_img = self.asset_loader.load_image("player", "player.png", scale=(30, 30))
        bullet_img = self.asset_loader.load_image("bullet", "player-bullet.png", scale=(settings.PLAYER_BULLET_SIZE, settings.PLAYER_BULLET_SIZE))
        self.enemy_bullet_img = self.asset_loader.load_image("enemy_bullet", "enemy-bullet.png", scale=(settings.ENEMY_BULLET_SIZE, settings.ENEMY_BULLET_SIZE))
        self.player = Player(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 50, player_img, bullet_img, self.sound_shoot)
        self.player_group.add(self.player)
        
        # Explosion
        self.explosion_img = self.asset_loader.load_image("explosion", "enemy-explosion.png", scale=(40, 40))
        
        # Enemy Manager
        self.enemy_manager = EnemyManager(self.enemy_group, self.level_manager.enemy_speed)
        self.level_manager.spawn_enemies(self.enemy_group)

        # Animated explosion
        self.explosion_sheet = self.asset_loader.load_image("explosion_sheet", "explosion-sheet.png")
        self.explosion_group = pygame.sprite.Group()

        # Scoring system
        self.font = pygame.font.Font(None, 24)
        self.score = 0
        self.lives = 3
        self.heart_size = (48, 48) 
        self.heart_img = self.asset_loader.load_image("heart", "heart.png", scale=self.heart_size)

    def run(self):
        while self.running:
            self.clock.tick(settings.FPS)
            self.event_handler.handle()

            if self.state == "playing":
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
                self.update()
                self.draw()

            elif self.state == "paused":
                pygame.mixer.music.pause()
                self.draw_paused()

            elif self.state == "game_over":
                pygame.mixer.music.pause()
                self.draw_game_over()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Update enemy movement as a group
        self.enemy_manager.update()
        self.bullet_group.update()
        self.enemy_bullet_group.update()
        self.explosion_group.update()

        # Player bullets hitting enemies
        for bullet in self.bullet_group:
        for bullet in self.bullet_group:
            hit_enemies = pygame.sprite.spritecollide(bullet, self.enemy_group, False)
            for enemy in hit_enemies:
                if enemy.hit():
                    self.score += 100
                    self.spawn_explosion(enemy.rect.centerx, enemy.rect.centery)
                    self.sound_explosion.play()
                bullet.kill()
            if hit_enemies:
                for enemy in hit_enemies:
                    explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, self.explosion_img)
                    self.explosion_group.add(explosion)
                bullet.kill()
                self.score += 10 * len(hit_enemies)  # Add 10 points per enemy
                self.sound_explosion.play()

        # Enemy shooting (bottom row only)
        for enemy in self.enemy_manager.get_bottom_enemies():
            if enemy.can_shoot(self.level_manager.enemy_shoot_prob):
                bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom, self.enemy_bullet_img)
                self.enemy_bullet_group.add(bullet)
                self.sound_enemy_shoot.play()

        # Enemy bullets hitting player
        if pygame.sprite.spritecollide(self.player, self.enemy_bullet_group, True):
            self.lives -= 1
            print(f"Player hit! Lives remaining: {self.lives}")
            if self.lives <= 0:
                self.state = "game_over"
                self.sound_game_over.play()

        # Level complete — load next level
        if not self.enemy_group:
            print("🎉 Level cleared! Showing transition...")

            # Fade out background music
            pygame.mixer.music.fadeout(500)

            # Show level complete screen
            self.draw_level_complete()

            # Play victory jingle
            self.sound_victory.set_volume(1.0)
            self.sound_victory.play()

            # Wait for jingle to finish (but allow window to update)
            duration = int(self.sound_victory.get_length() * 1000)
            start_time = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start_time < duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        return
                # Keep showing the transition screen
                self.draw_level_complete()
                self.clock.tick(settings.FPS)

            # Next level
            self.level_manager.next_level(self.enemy_group)
            self.enemy_manager.speed = self.level_manager.enemy_speed

            # Resume background music
            pygame.mixer.music.load("assets/sounds/background-music.ogg")
            pygame.mixer.music.play(-1)

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))

        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        restart_text = self.font.render("Press R to Restart", True, (255, 255, 255))
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 0))

        self.screen.blit(game_over_text, self._center(game_over_text, y_offset=-40))
        self.screen.blit(score_text, self._center(score_text))
        self.screen.blit(restart_text, self._center(restart_text, y_offset=40))

        pygame.display.flip()

    def restart(self):
        self.score = 0
        self.flash_timer = 0
        self.state = "playing"

        self.player.rect.centerx = settings.SCREEN_WIDTH // 2
        self.bullet_group.empty()
        self.enemy_bullet_group.empty()
        self.enemy_group.empty()
        self.level_manager.level = 1
        self.level_manager.enemy_speed = settings.INITIAL_ENEMY_SPEED
        self.level_manager.enemy_shoot_prob = settings.INITIAL_ENEMY_SHOOT_PROB
        self.enemy_manager.speed = self.level_manager.enemy_speed
        self.level_manager.spawn_enemies(self.enemy_group)
    
    def draw(self):
        self.screen.fill((0, 0, 30))  # Dark blue background
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.enemy_bullet_group.draw(self.screen)
        self.explosion_group.draw(self.screen)  # 💥 Draw explosions here!

        # Show the score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Show the current level (top-centre)
        level_text = self.font.render(f"Level {self.level_manager.level}", True, (0, 255, 255))
        level_rect = level_text.get_rect(midtop=(settings.SCREEN_WIDTH // 2, 10))
        self.screen.blit(level_text, level_rect)        

        # show the hearts - number of lives left (top-right)
        heart_width, heart_height = self.heart_size
        for i in range(self.lives):
            # Draw hearts from right to left
            x = settings.SCREEN_WIDTH - (i + 1) * (heart_width//2 + 20)
            self.screen.blit(self.heart_img, (x, 0))

        # when hitting the target
        self.explosion_group.draw(self.screen)

        # Pause hint - bottom right
        pause_hint = self.font.render("Press P to Pause", True, (200, 200, 200))
        pause_rect = pause_hint.get_rect(bottomright=(settings.SCREEN_WIDTH - 10, settings.SCREEN_HEIGHT - 10))
        self.screen.blit(pause_hint, pause_rect)
        
        pygame.display.flip()

    def draw_paused(self):
        self.screen.fill((0, 0, 30))

        pause_text = self.font.render("PAUSED", True, (255, 255, 0))
        instructions = self.font.render("Press P to Resume", True, (255, 255, 255))

        self.screen.blit(pause_text, self._center(pause_text, y_offset=-20))
        self.screen.blit(instructions, self._center(instructions, y_offset=20))

        pygame.display.flip()

    def draw_level_complete(self):
        self.screen.fill((0, 0, 30))

        msg = f"Level {self.level_manager.level} Complete!"
        complete_text = self.font.render(msg, True, (255, 255, 0))
        info_text = self.font.render("Get ready for the next wave...", True, (255, 255, 255))

        self.screen.blit(complete_text, self._center(complete_text, y_offset=-20))
        self.screen.blit(info_text, self._center(info_text, y_offset=30))

        pygame.display.flip()

    def _center(self, surface, y_offset=0):
        rect = surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + y_offset))
        return rect
