import pygame
import config as config
from snake import Snake
from food import Food
from gamestate import GameState
from hud import HUD
from input_handler import InputHandler
from game_controller import GameController

class Game:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        pygame.display.set_caption("Snake Game")

        self.menu_font = pygame.font.SysFont(None, config.MENU_FONT_SIZE)
        self.font = pygame.font.SysFont(None, config.FONT_SIZE)
        self.hud = HUD(self.font)
        self.input_handler = InputHandler(self)
        self.controller = GameController(self)

        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.food.reset(self.snake.body)

        self.sounds = {
            "eat": pygame.mixer.Sound("assets/sounds/eat.ogg"),
            "game_over": pygame.mixer.Sound("assets/sounds/game_over.ogg"),
            "start": pygame.mixer.Sound("assets/sounds/start.ogg"),
        }
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT + config.HEADER_HEIGHT))
        self.score = 0
        self.state = GameState.MENU
        self.last_move_time = pygame.time.get_ticks()
        self.move_delay = config.MOVE_DELAY_START
        self.running = True

        self.background = pygame.image.load("assets/background.png").convert()
        self.background = pygame.transform.scale(self.background, (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

    @property
    def level(self):
        return (self.score // config.SPEED_UP_EVERY) + 1

    def show_main_menu(self):
        self.screen.fill((20, 20, 50))
        title_text = self.menu_font.render("Snake Game", True, (0, 255, 150))
        prompt_text = self.font.render("Press SPACE to Start", True, (200, 200, 255))
        title_rect = title_text.get_rect(center=(config.WINDOW_WIDTH // 2, (config.WINDOW_HEIGHT + config.HEADER_HEIGHT) // 2 - 40))
        prompt_rect = prompt_text.get_rect(center=(config.WINDOW_WIDTH // 2, (config.WINDOW_HEIGHT + config.HEADER_HEIGHT) // 2 + 10))
        self.screen.blit(title_text, title_rect)
        self.screen.blit(prompt_text, prompt_rect)
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.input_handler.handle_event(event)

            current_time = pygame.time.get_ticks()

            if self.state == GameState.MENU:
                self.show_main_menu()
                self.clock.tick(config.FPS)
                continue

            if self.state == GameState.PLAYING:
                if current_time - self.last_move_time > self.move_delay:
                    self.snake.move()
                    self.controller.check_collision()
                    if self.controller.check_game_over():
                        self.state = GameState.GAME_OVER
                    self.last_move_time = current_time

            self.screen.fill(config.BLACK)
            self.screen.blit(self.background, (0, config.HEADER_HEIGHT))
            self.hud.draw_score_panel(self.screen, self.score, self.level)
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            if self.state == GameState.GAME_OVER:
                self.hud.draw_game_over(self.screen)
            elif self.state == GameState.PAUSED:
                self.hud.draw_pause_overlay(self.screen)

            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()

    @property
    def level(self):
        return (self.score // config.SPEED_UP_EVERY) + 1
        