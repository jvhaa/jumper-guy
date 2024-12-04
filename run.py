import pygame
import sys

class main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((400, 300))
        
        self.clock = pygame.time.Clock()
        self.gamestate = "game"
        
    def game_handler(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.display.blit()


main().game_handler()