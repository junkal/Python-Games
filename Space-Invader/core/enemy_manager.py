# core/enemy_manager.py
from pygame.sprite import Group
from core.settings import SCREEN_WIDTH

class EnemyManager:
    def __init__(self, group: Group, speed=2):
        self.group = group
        self.direction = 1
        self.speed = speed

    def update(self):
        dx = self.speed * self.direction
        dy = 0

        # Check if any enemy hits screen edge
        for enemy in self.group:
            if enemy.rect.right + dx >= SCREEN_WIDTH or enemy.rect.left + dx <= 0:
                self.direction *= -1
                dy = 20
                dx = self.speed * self.direction
                break

        for enemy in self.group:
            dx = enemy.base_speed * self.direction
            enemy.update(dx, dy)

    def get_bottom_enemies(self):
        """
        Returns a list of the lowest enemy in each column.
        """
        columns = {}
        for enemy in self.group:
            col_key = round(enemy.rect.centerx / 10)  # Bucket enemies by horizontal position
            if col_key not in columns or enemy.rect.bottom > columns[col_key].rect.bottom:
                columns[col_key] = enemy

        return list(columns.values())