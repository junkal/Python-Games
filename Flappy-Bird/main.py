import pygame
from settings import WIDTH, HEIGHT
from game import Game
from assets import Assets

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    assets = Assets()
    game = Game(screen, assets)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()