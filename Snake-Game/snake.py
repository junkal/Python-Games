import pygame
from segment import SnakeSegment

class Snake:
    def __init__(self):
        self.segments = pygame.sprite.Group()
        self.positions = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self._create_segments()

    def _create_segments(self):
        self.segments.empty()
        for i, (x, y) in enumerate(self.positions):
            self.segments.add(SnakeSegment(x, y, is_head=(i == 0)))

    def move(self):
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.positions = [new_head] + self.positions[:-1]

        for i, (segment, new_pos) in enumerate(zip(self.segments.sprites(), self.positions)):
            segment.grid_position = new_pos
            if i == 0:
                segment.direction = self.direction  # Pass direction to the head
            segment.update_position()

    def grow(self):
        tail = self.positions[-1]
        self.positions.append(tail)
        segment = SnakeSegment(*tail, is_head=False)
        self.segments.add(segment)

    def change_direction(self, direction):
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.direction = direction

    def draw(self, surface):
        self.segments.draw(surface)

    def reset(self):
        self.positions = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self._create_segments()

    @property
    def body(self):
        return self.positions