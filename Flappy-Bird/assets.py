import pygame
import os
from settings import ASSET_DIR, WIDTH, HEIGHT, BIRD_WIDTH, BIRD_HEIGHT, PIPE_WIDTH

class Assets:
    def __init__(self):
        self.images = {}
        self.load_assets()

    def load_image(self, filename, size=None, flip=False):
        path = os.path.join(ASSET_DIR, filename)
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        if flip:
            image = pygame.transform.flip(image, False, True)
        return image

    def load_assets(self):
        self.images['background'] = self.load_image('background.png', (WIDTH, HEIGHT))
        self.images['bird_1'] = self.load_image('bird-1.png', (BIRD_WIDTH, BIRD_HEIGHT))
        self.images['bird_2'] = self.load_image('bird-2.png', (BIRD_WIDTH, BIRD_HEIGHT))
        self.images['pipe-1'] = self.load_image('pipe-1.png', (PIPE_WIDTH, 500))
        self.images['pipe-2'] = self.load_image('pipe-2.png', (PIPE_WIDTH, 500))        # Optional:
        # self.images['base'] = self.load_image('base.png', (WIDTH, 100))

        self.sounds = {}
        self.sounds['flap'] = pygame.mixer.Sound(os.path.join(ASSET_DIR, 'flap.mp3'))
        self.sounds['score'] = pygame.mixer.Sound(os.path.join(ASSET_DIR, 'score.mp3'))
        self.sounds['hit'] = pygame.mixer.Sound(os.path.join(ASSET_DIR, 'hit.mp3'))

    def get(self, name):
        return self.images[name]