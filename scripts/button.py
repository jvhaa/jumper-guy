import pygame

class textbox():
    def __init__(self, game, surf, coords, images):
        self.game = game
        self.surf = surf
        self.coords = coords
        self.images = images
        self.rect = pygame.Rect(coords[0], coords[1], images[0].get_width(), images[0].get_height())

    def update(self):
        variant = 0
        if self.rect.collidepoint(self.game.mx, self.game.my):
            variant = 1
            if self.game.click == True:
                self.game.transiton = True
        if variant == 0:
            self.surf.blit(self.images[variant], self.coords)
        else:
            self.surf.blit(self.images[variant], (self.coords[0]-2, self.coords[1]-2))