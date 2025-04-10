import pygame
import config

class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, x, y, is_head=False):
        super().__init__()
        self.is_head = is_head
        self.direction = (1, 0)  # Default direction
        self.grid_position = (x, y)

        if is_head:
            self.original_image = pygame.image.load("assets/snake_head.png").convert_alpha()
            scale = int(config.CELL_SIZE * 1.2)
            self.original_image = pygame.transform.scale(self.original_image, (scale, scale))
            self.image = self.original_image
        else:
            body_image = pygame.image.load("assets/snake_body.png").convert_alpha()
            scale = int(config.CELL_SIZE * 0.8)
            self.image = pygame.transform.scale(body_image, (scale, scale))

        self.rect = self.image.get_rect(center=(x * config.CELL_SIZE + config.CELL_SIZE // 2, y * config.CELL_SIZE + config.CELL_SIZE // 2))

    def update_position(self):
        self.rect.center = (
            self.grid_position[0] * config.CELL_SIZE + config.CELL_SIZE // 2,
            self.grid_position[1] * config.CELL_SIZE + config.CELL_SIZE // 2
        )
        if self.is_head:
            angle = self.direction_to_angle(self.direction)
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    @staticmethod
    def direction_to_angle(direction):
        if direction == (0, -1):   # Up
            return 180
        elif direction == (1, 0):  # Right
            return 90
        elif direction == (0, 1):  # Down
            return 0
        elif direction == (-1, 0): # Left
            return -90
        return 0