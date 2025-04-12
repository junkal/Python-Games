import config as config
from gamestate import GameState

class GameController:
    def __init__(self, game):
        self.game = game

    def reset(self):
        self.game.snake.reset()
        self.game.food.reset(self.game.snake.body)
        self.game.score = 0
        self.game.move_delay = config.MOVE_DELAY_START
        self.game.state = GameState.PLAYING

    def check_collision(self):
        if self.game.snake.body[0] == self.game.food.grid_position:
            self.game.snake.grow()
            self.game.food.reset(self.game.snake.body)
            self.game.score += 10
            self.game.sounds["eat"].play()

            if self.game.score % config.SPEED_UP_EVERY == 0:
                self.game.move_delay = max(config.MOVE_DELAY_MIN,
                                           self.game.move_delay - config.DELAY_STEP)

    def check_game_over(self):
        for segment in self.game.snake.body:
            x, y = segment
            if x <= 0 or x >= config.WINDOW_WIDTH // config.CELL_SIZE:
                self.game.sounds["game_over"].play()
                return True
            if y >= (config.WINDOW_HEIGHT + config.HEADER_HEIGHT) // config.CELL_SIZE:
                self.game.sounds["game_over"].play()
                return True
            if y < config.HEADER_HEIGHT // config.CELL_SIZE:
                self.game.sounds["game_over"].play()
                return True

        head = self.game.snake.body[0]
        if head in self.game.snake.body[1:]:
            self.game.sounds["game_over"].play()
            return True
        return False