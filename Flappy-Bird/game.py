import pygame
from bird import Bird
from pipe import PipePair
from settings import WIDTH, HEIGHT, WHITE, FPS

class Game:
    def __init__(self, screen, assets): 
        self.screen = screen
        self.assets = assets
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.bg = self.assets.get('background')

        self.bird = Bird(100, HEIGHT // 2, self.assets)
        self.pipes = []
        self.frame_count = 0
        self.score = 0

        # Floating score text
        self.floating_texts = []

        self.running = True
        self.playing = False
        self.paused = False
        self.game_over_cooldown = 0

    def reset_game(self):
        self.bird = Bird(100, HEIGHT // 2, self.assets)
        self.pipes = []
        self.frame_count = 0
        self.score = 0
        self.floating_texts = []

    def spawn_pipes(self):
        if self.frame_count % 90 == 0:
            self.pipes.append(PipePair(WIDTH, self.assets))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.playing:
                        self.playing = True
                        self.reset_game()
                    elif not self.paused:
                        self.bird.start_flap(self.frame_count)
                    self.assets.sounds['flap'].play()
                elif event.key == pygame.K_p and self.playing:
                    self.paused = not self.paused
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and self.playing and not self.paused:
                    self.bird.end_flap(self.frame_count)

    def update(self):
        if not self.paused and self.playing:
            self.spawn_pipes()
            self.bird.update()

            for pipe in self.pipes:
                pipe.move()

                if pipe.collides_with(self.bird.rect):
                    self.assets.sounds['hit'].play()
                    self.game_over_cooldown = 60
                    self.playing = False  # Game over
                    break

                if not pipe.passed and pipe.top.x + pipe.top.width < self.bird.rect.x:
                    pipe.passed = True
                    self.score += 10
                    self.assets.sounds['score'].play()
                    self.floating_texts.append({
                        'text': '+10',
                        'x': self.bird.rect.x,
                        'y': self.bird.rect.y,
                        'timer': 30
                    })

            self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

            if self.bird.rect.top <= 0 or self.bird.rect.bottom >= HEIGHT:
                self.assets.sounds['hit'].play()
                self.playing = False

            self.frame_count += 1

        # Floating texts animation
        for ft in self.floating_texts[:]:
            ft['y'] -= 1
            ft['timer'] -= 1
            if ft['timer'] <= 0:
                self.floating_texts.remove(ft)
    
    def draw_start_screen(self):
        self.screen.blit(self.bg, (0, 0))
        text = self.font.render("Press SPACE to Start", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 30))
        pygame.display.flip()

    def draw_game_over_screen(self):
        self.screen.blit(self.bg, (0, 0))
        text1 = self.font.render("Game Over", True, WHITE)
        text2 = self.font.render(f"Score: {self.score}", True, WHITE)
        text3 = self.font.render("Press SPACE to Retry", True, WHITE)
        pause_hint = self.font.render("Press P to pause", True, WHITE)

        self.screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 60))
        self.screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - 10))
        self.screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 40))
        self.screen.blit(pause_hint, (WIDTH - pause_hint.get_width() - 10, HEIGHT - pause_hint.get_height() - 10))
        pygame.display.flip()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        for pipe in self.pipes:
            pipe.draw(self.screen)

        self.bird.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.paused:
            pause_text = self.font.render("Paused", True, WHITE)
            self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

        # Draw pause hint
        pause_hint = self.font.render('Press P to pause', True, WHITE)
        self.screen.blit(pause_hint, (WIDTH - pause_hint.get_width() - 10, HEIGHT - pause_hint.get_height() - 10))

        # Draw floating score animations
        for ft in self.floating_texts[:]:
            text_surface = self.font.render(ft['text'], True, WHITE)
            self.screen.blit(text_surface, (ft['x'], ft['y']))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            if not self.playing:
                if self.frame_count > 0:
                    if self.game_over_cooldown == 0:
                        self.draw_game_over_screen()
                    # Countdown to allow hit delay before game over screen
                    else:
                        self.game_over_cooldown -= 1
                else:
                    self.draw_start_screen()
            else:
                self.update()
                self.draw()