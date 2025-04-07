import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, image, duration=15):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = duration  # number of frames it lasts

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()