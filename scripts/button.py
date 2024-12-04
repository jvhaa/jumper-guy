from scripts.text import text, textindex
import pygame

class textbox():
    def __init__(self, game, surf, coords, text, type):
        self.game = game
        self.surf = surf
        coords = coords
        self.msg = text
        textl = self.textlength(game, text)
        size = (textl+10, 16)
        self.textcoords = (coords[0]+6, coords[1]+2)
        self.rect = pygame.Rect(coords, size)
        self.rect2 = pygame.Rect(coords[0]+1, coords[1]+1, size[0]-2, size[1]-2)
        self.type = type

    def textlength(self, game, text):
        width = 0
        for word in text:
            width += game.assets["alphabet"][textindex.index(word)].get_width() + 2
        return width

    def update(self):
        colour = (255, 0, 0)
        variant = "normal"
        if self.rect.collidepoint(self.game.mx, self.game.my):
            colour = (0, 255, 0) 
            variant = "special"
            if self.game.click == True:
                self.game.gamestate = self.type
                if self.type[:4] == "game" and len(self.type) > 4:
                    self.game.gamestate = "game"
                    self.game.load_map(int(self.type.split(" ")[1])-1)

                self.game.b()
        pygame.draw.rect(self.surf, colour, self.rect)
        pygame.draw.rect(self.surf, (0, 0, 0), self.rect2)
        text(self.game, self.surf, self.textcoords, self.msg, variant)