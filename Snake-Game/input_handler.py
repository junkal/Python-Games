import pygame
from enum import Enum
from gamestate import GameState

class InputHandler:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False

        elif event.type == pygame.KEYDOWN:
            if self.game.state == GameState.MENU:
                if event.key == pygame.K_SPACE:
                    self.game.sounds["start"].play()
                    self.game.controller.reset() 
            elif self.game.state == GameState.GAME_OVER:
                if event.key == pygame.K_r:
                    self.game.controller.reset()
            elif self.game.state == GameState.PLAYING:
                if event.key == pygame.K_p:
                    self.game.state = GameState.PAUSED
                elif event.key == pygame.K_UP:
                    self.game.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.game.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.game.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.game.snake.change_direction((1, 0))
            elif self.game.state == GameState.PAUSED:
                if event.key == pygame.K_p:
                    self.game.state = GameState.PLAYING