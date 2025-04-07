import pygame
from core.settings import ENEMY_BULLET_SPEED

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += ENEMY_BULLET_SPEED
        if self.rect.top > 600:
            self.kill()