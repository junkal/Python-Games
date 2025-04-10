import pygame
import config as config
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT + config.HEADER_HEIGHT))
        icon_surface = pygame.Surface((32, 32))
        icon_surface.fill(config.WHITE)
        pygame.display.set_icon(icon_surface)
        pygame.display.set_caption("Snake Game")
        self.menu_font = pygame.font.SysFont(None, config.MENU_FONT_SIZE)
        self.font = pygame.font.SysFont(None, config.FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.food.reset(self.snake.body)
        self.score = 0
        self.last_move_time = pygame.time.get_ticks()
        self.move_delay = config.MOVE_DELAY_START
        self.running = True
        self.show_menu = True
        self.paused = False
        self.game_over = False
        self.background = pygame.image.load("assets/background.png").convert()
        self.background = pygame.transform.scale(self.background, (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

    def reset(self):
        self.snake.reset()
        self.food.reset(self.snake.body)
        self.score = 0
        self.game_over = False

    def check_collision(self):
        if self.snake.body[0] == self.food.grid_position:
            self.snake.grow()
            self.food.reset(self.snake.body)
            self.score += 10

            # Decrease move delay every few points
            if self.score % config.SPEED_UP_EVERY == 0:
                self.move_delay = max(config.MOVE_DELAY_MIN, self.move_delay - config.DELAY_STEP)

    def check_game_over(self):
        for segment in self.snake.body:
            x, y = segment

            if x <= 0 or x >= config.WINDOW_WIDTH // config.CELL_SIZE:
                return True
            if y >= (config.WINDOW_HEIGHT + config.HEADER_HEIGHT) // config.CELL_SIZE:
                return True
            if y <= config.HEADER_HEIGHT // config.CELL_SIZE:
                return True

        head = self.snake.body[0]
        if head in self.snake.body[1:]:
            return True

        return False

    def draw_score_panel(self):
        pygame.draw.rect(self.screen, (20, 20, 20), (0, 0, config.WINDOW_WIDTH, config.HEADER_HEIGHT))
        pygame.draw.line(self.screen, config.WHITE, (0, config.HEADER_HEIGHT), (config.WINDOW_WIDTH, config.HEADER_HEIGHT), 2)

        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 180))
        level_surface = self.font.render(f"Level: {self.level}", True, (180, 255, 180))

        self.screen.blit(score_surface, (10, 10))
        self.screen.blit(level_surface, (200, 10))

        pause_hint_surface = self.font.render("Press 'P' to pause game", True, (180, 180, 180))
        pause_rect = pause_hint_surface.get_rect(
            bottomright=(config.WINDOW_WIDTH - 10, config.WINDOW_HEIGHT + config.HEADER_HEIGHT - 10)
        )
        self.screen.blit(pause_hint_surface, pause_rect)        
    
    def draw_game_over(self):
        text = self.font.render("Game Over! Press R to Restart", True, (255, 80, 80))
        rect = text.get_rect(center=(config.WINDOW_WIDTH // 2, (config.WINDOW_HEIGHT + config.HEADER_HEIGHT) // 2))
        self.screen.blit(text, rect)

    def draw_pause_overlay(self):
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT + config.HEADER_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # semi-transparent dark overlay

        text = self.font.render("Paused - Press P to Resume", True, (255, 255, 255))
        text_rect = text.get_rect(center=(config.WINDOW_WIDTH // 2, (config.WINDOW_HEIGHT + config.HEADER_HEIGHT) // 2))

        overlay.blit(text, text_rect)
        self.screen.blit(overlay, (0, 0))

    def show_main_menu(self):
        self.screen.fill((20, 20, 50))
        title_text = self.menu_font.render("Snake Game", True, (0, 255, 150))
        prompt_text = self.font.render("Press SPACE to Start", True, (200, 200, 255))
        title_rect = title_text.get_rect(center=(config.WINDOW_WIDTH // 2, (config.WINDOW_HEIGHT + config.HEADER_HEIGHT) // 2 - 40))
        prompt_rect = prompt_text.get_rect(center=(config.WINDOW_WIDTH // 2, (config.WINDOW_HEIGHT + config.HEADER_HEIGHT) // 2 + 10))
        self.screen.blit(title_text, title_rect)
        self.screen.blit(prompt_text, prompt_rect)
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if self.show_menu:
                if event.key == pygame.K_SPACE:
                    self.show_menu = False
                    self.reset()
            elif self.game_over:
                if event.key == pygame.K_r:
                    self.reset()
            else:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_input(event)

            if self.show_menu:
                self.show_main_menu()
                self.clock.tick(config.FPS)
                continue

            current_time = pygame.time.get_ticks()

            if not self.game_over and not self.paused:
                if current_time - self.last_move_time > self.move_delay:
                    self.snake.move()
                    self.check_collision()
                    if self.check_game_over():
                        self.game_over = True
                    self.last_move_time = current_time

            self.screen.fill((0, 0, 0)) 
            self.screen.blit(self.background, (0, config.HEADER_HEIGHT)) 
            self.draw_score_panel()

            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            if self.paused:
                self.draw_pause_overlay()

            if self.game_over:
                self.draw_game_over()
            pygame.display.flip()
            self.clock.tick(config.FPS)
        
        pygame.quit()

    @property
    def level(self):
        return (self.score // config.SPEED_UP_EVERY) + 1
        