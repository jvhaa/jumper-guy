from scripts.text import text, textindex
import pygame

class textbox():
    def __init__(self, game, surf, coords, images, type):
        self.game = game
        self.surf = surf
        coords = coords
        self.images = images
        self.type = type

    def update(self):
        variant = 0
        if self.rect.collidepoint(self.game.mx, self.game.my):
            variant = 1
            if self.game.click == True:
                self.game.gamestate = self.type
                if self.type[:4] == "game" and len(self.type) > 4:
                    self.game.gamestate = "game"
                    self.game.load_map(int(self.type.split(" ")[1])-1)

                self.game.b()
        self.surf.blit(self.images[variant])