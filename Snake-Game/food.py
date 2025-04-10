import pygame
import random
import config

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (config.CELL_SIZE, config.CELL_SIZE))
        self.rect = self.image.get_rect()
        self.reset()

    def random_position(self):
        cols = config.WINDOW_WIDTH // config.CELL_SIZE
        rows = config.WINDOW_HEIGHT // config.CELL_SIZE

        min_x = config.SAFE_MARGIN
        max_x = cols - 1 - config.SAFE_MARGIN

        min_y = (config.HEADER_HEIGHT // config.CELL_SIZE) + config.SAFE_MARGIN
        max_y = rows - 1 - config.SAFE_MARGIN

        return random.randint(min_x, max_x), random.randint(min_y, max_y)

    def reset(self, snake_body=None):
        while True:
            pos = self.random_position()
            if not snake_body or pos not in snake_body:
                break
        self.grid_position = pos
        self.rect.topleft = (pos[0] * config.CELL_SIZE, pos[1] * config.CELL_SIZE)

    def draw(self, surface):
        surface.blit(self.image, self.rect)