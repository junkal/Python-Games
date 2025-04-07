# entities/player.py
import pygame
from core.settings import PLAYER_SPEED
from entities.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, bullet_image, shoot_sound):
        super().__init__()
        self.image = image
        self.bullet_image = bullet_image
        self.shoot_sound = shoot_sound
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += PLAYER_SPEED

    def shoot(self, bullet_group):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_image)
        bullet_group.add(bullet)
        self.shoot_sound.play()