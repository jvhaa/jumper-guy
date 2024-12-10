'''
    items.py 

    Item handler, used for idk handling items lol

    Functions:
        Item(game, coords, type, size, speed) -> Item
        update() -> pygame.Rect
        render(camdiff) -> None
        touched() -> None
'''

import pygame

class Item:
    def __init__(self, game, coords, type, size, speed):
        self.game = game
        self.coords = coords
        self.type = type
        self.img = game.assets[type]
        self.dir = "up"
        self.lim = self.coords[1] - 10
        self.lim2 = self.coords[1]
        self.surf = game.display
        self.size = size
        self.speed = speed
    
    def update(self):
        if self.dir == "up":
            self.coords[1] += self.speed
        else:
            self.coords[1] -= self.speed
        
        if self.coords[1] > self.lim2:
            self.dir = "down"
        elif self.coords[1] < self.lim:
            self.dir = "up"
        return pygame.Rect(self.coords[0], self.coords[1], self.size[0], self.size[1])

    
    def render(self, camdiff):
        # Render the object on the screen
        self.surf.blit(self.img, (self.coords[0]-camdiff[0], self.coords[1]-camdiff[1]))

    def touched(self):

        # heal player when touched
        if self.type == "heal":
            self.game.player.hp = min(self.game.player.hp+1, 6)


        # load next level when touched
        if self.type == "chest":
            self.game.transiton = True

        
