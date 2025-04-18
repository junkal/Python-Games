
import pygame
import random
from settings import HEIGHT, PIPE_WIDTH, PIPE_SPEED, MIN_PIPE_GAP, MAX_PIPE_GAP

class PipePair:
    def __init__(self, x, assets):
        chosen_pipe_name = random.choice(['pipe-1', 'pipe-2'])
        raw_pipe_img = assets.get(chosen_pipe_name)

        self.pipe_img = pygame.transform.scale(raw_pipe_img, (PIPE_WIDTH, 500))
        self.pipe_img_flipped = pygame.transform.flip(self.pipe_img, False, True)

        gap = random.randint(MIN_PIPE_GAP, MAX_PIPE_GAP)
        self.top_height = random.randint(50, HEIGHT - gap - 50)

        self.top = pygame.Rect(x, 0, PIPE_WIDTH, self.top_height)
        self.top.inflate_ip(-24, 0)  # Shrinks width and height slightly

        self.bottom = pygame.Rect(x, self.top_height + gap, PIPE_WIDTH, HEIGHT)
        self.bottom.inflate_ip(-24, 0)  # Shrinks width and height slightly

        self.passed = False

    def move(self):
        self.top.x -= PIPE_SPEED
        self.bottom.x -= PIPE_SPEED

    def draw(self, screen):
        screen.blit(self.pipe_img_flipped, (self.top.x, self.top.bottom - self.pipe_img_flipped.get_height()))
        screen.blit(self.pipe_img, (self.bottom.x, self.bottom.y))

    def off_screen(self):
        return self.top.right < 0

    def collides_with(self, bird_rect, bird_mask=None):
        return bird_rect.colliderect(self.top) or bird_rect.colliderect(self.bottom)
