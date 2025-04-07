from entities.enemy import Enemy
import core.settings as settings
import random

class LevelManager:
    def __init__(self, asset_loader):
        self.level = 1
        self.enemy_speed = settings.INITIAL_ENEMY_SPEED
        self.enemy_shoot_prob = settings.INITIAL_ENEMY_SHOOT_PROB
        self.asset_loader = asset_loader

    def next_level(self, enemy_group, enemy_images):  # 🛠 Added enemy_images
        self.level += 1
        self.enemy_speed += 0.5
        self.enemy_shoot_prob += 0.001
        self.spawn_enemies(enemy_group, enemy_images)  # 🛠 Pass it here too

    def spawn_enemies(self, group, enemy_images):
        rows = min(3 + self.level, 6)
        cols = 8
        spacing_x = 60
        spacing_y = 60

        for row in range(rows):
            for col in range(cols):
                x = col * spacing_x + 60
                y = row * spacing_y + 40

                # 🎲 Randomly assign variant with weighted probabilities
                variant = self.choose_variant()

                enemy = Enemy(x, y, enemy_images[variant], variant, speed=self.enemy_speed)
                group.add(enemy)

    def choose_variant(self):
        """Choose enemy variant based on current level with weights."""
        weights = {
            'basic': max(0.6 - self.level * 0.05, 0.2),
            'fast': min(0.25 + self.level * 0.03, 0.5),
            'tanky': min(0.15 + self.level * 0.02, 0.4)
        }
        variants = list(weights.keys())
        probs = list(weights.values())
        return random.choices(variants, probs, k=1)[0]