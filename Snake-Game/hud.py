import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, HEADER_HEIGHT, WHITE

class HUD:
    def __init__(self, font):
        self.font = font

    def draw_score_panel(self, screen, score, level):
        pygame.draw.rect(screen, (20, 20, 20), (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))
        pygame.draw.line(screen, WHITE, (0, HEADER_HEIGHT), (WINDOW_WIDTH, HEADER_HEIGHT), 2)

        score_surface = self.font.render(f"Score: {score}", True, (255, 255, 180))
        level_surface = self.font.render(f"Level: {level}", True, (180, 255, 180))
        pause_hint_surface = self.font.render("P: Pause", True, (180, 180, 180))

        screen.blit(score_surface, (10, 10))
        screen.blit(level_surface, (200, 10))
        screen.blit(pause_hint_surface, (WINDOW_WIDTH - 80, WINDOW_HEIGHT + HEADER_HEIGHT - 20))

    def draw_pause_overlay(self, screen):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + HEADER_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        text = self.font.render("Paused - Press P to Resume", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT + HEADER_HEIGHT) // 2))
        overlay.blit(text, text_rect)
        screen.blit(overlay, (0, 0))

    def draw_game_over(self, screen):
        text = self.font.render("Game Over! Press R to Restart", True, (255, 80, 80))
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT + HEADER_HEIGHT) // 2))
        screen.blit(text, rect)