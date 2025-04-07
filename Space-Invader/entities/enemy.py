import pygame
from random import random

ENEMY_STATS = {
    'basic': {
        'speed_multiplier': 1.0,
        'hp': 1
    },
    'fast': {
        'speed_multiplier': 2.0,
        'hp': 1
    },
    'tanky': {
        'speed_multiplier': 0.5,
        'hp': 3
    }
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, variant='basic', speed=1):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.variant = variant
        self.direction = 1  # 1 = right, -1 = left

        stats = ENEMY_STATS.get(variant, ENEMY_STATS['basic'])
        self.hp = stats['hp']
        self.base_speed = speed * stats['speed_multiplier']

    def update(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy

    def reverse_direction_and_drop(self, drop_distance):
        self.direction *= -1
        self.rect.y += drop_distance

    def can_shoot(self, shoot_prob):
        return random() < shoot_prob

    def hit(self):
        """Call this when the enemy is hit by a bullet."""
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
            return True  # Enemy destroyed
        return False     # Still alive