'''
    button.py

    Basically animates the buttons on the screen,
    if its being hovered over, use the seccond image,

    Functions:
        textbox(game, surf, coords, images) -> textbox
        update() -> None
'''

import pygame

class textbox():
    def __init__(self, game, surf, coords, images):
        self.game = game
        self.surf = surf
        self.coords = coords
        self.images = images
        self.rect = pygame.Rect(coords[0], coords[1], images[0].get_width(), images[0].get_height())

    
    def update(self):
        variant = 0 # Default image
        if self.rect.collidepoint(self.game.mx, self.game.my):
            variant = 1 # Switch to the hover image
            if self.game.click == True:
                self.game.transiton = True

        

        if variant == 0:
            self.surf.blit(self.images[variant], self.coords) # Render the default image
        else:
            self.surf.blit(self.images[variant], (self.coords[0]-2, self.coords[1]-2)) # Render the hover image with a slight offset