import pygame

class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            # While playing
            elif self.game.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.player.shoot(self.game.bullet_group)
                    elif event.key == pygame.K_p:
                        self.game.state = "paused"

            # While paused
            elif self.game.state == "paused":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.game.state = "playing"

            elif self.game.state == "game_over":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.game.restart()