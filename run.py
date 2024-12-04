import pygame
import sys

class main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((400, 300))
        
        self.clock = pygame.time.Clock()
        self.gamestate = "game"
        self.assets = {
            
        }
        
    def game_handler(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.size()), (0,0))


main().game_handler()