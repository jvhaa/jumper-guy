import pygame
import sys

from scripts.clouds import Clouds
from scripts.entity import player, enemy
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import TileMap

class main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((400, 300))

        self.assets = {
            "clouds" : load_images("clouds"),
            "colliables": load_images("colliables")
        }
        
        self.clock = pygame.time.Clock()
        self.gamestate = "game"
        self.tilemap = TileMap(self, 50)
        self.level = 0
        self.clouds = Clouds(self.assets["clouds"])
        self.player = player(self, (0, 0), (20, 10))
        self.enemies = []
        
    def game_handler(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.gamestate == "game":
                self.game()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.size()), (0,0))
            

    def game(self):
        self.screen.blit(self.assets["background"], (0,0))
        self.player.update()
        self.player.render(self.display)

    
    def load_map(self, map_id):
        self.Tilemap.load("maps/" + str(map_id) + ".json")

        self.enemies = []
        self.sparks = []
        
        for spawner in self.Tilemap.extract([("spawner", 0), ("spawner", 1)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
            if spawner["variant"] == 0:
                self.eenmies.append(enemy(self, spawner["pos"], (50, 50)))
        


main().game_handler()