import pygame
from settings import BIRD_WIDTH, BIRD_HEIGHT, GRAVITY

class Bird:
    def __init__(self, x, y, assets):
        self.frames = [
            pygame.transform.scale(assets.get('bird_1'), (
                int(BIRD_WIDTH * 2),
                int(BIRD_HEIGHT * 2)
            )),
            pygame.transform.scale(assets.get('bird_2'), (
                int(BIRD_WIDTH * 2),
                int(BIRD_HEIGHT * 2)
            ))
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.image = self.frames[0]

        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.inflate_ip(-6, -6)
        self.velocity = 0

        self.jump_start_frame = None
        self.holding_jump = False

    def start_flap(self, frame_count):
        self.jump_start_frame = frame_count
        self.holding_jump = True

    def end_flap(self, frame_count):
        if self.holding_jump:
            hold_duration = frame_count - self.jump_start_frame
            force = max(-10, -4 - hold_duration * 0.5)
            self.velocity = force
            self.holding_jump = False

    def update(self):
        self.velocity += GRAVITY
        self.velocity = min(self.velocity, 10)
        self.rect.y += int(self.velocity)

        # Animate flapping
        self.frame_timer += 1
        if self.frame_timer % 5 == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)