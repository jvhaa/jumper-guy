import pygame
import random

'''
    This file is left unused.
    It is a part of the old version of the game.
    
    Cloud renderer
'''

class cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = pos
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed
    
    def render(self, surf, offset = (0, 0)):
        render_pos = ((self.pos[0] - offset[0])*self.depth, (self.pos[1]-offset[1])*self.depth)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))

class Clouds:
    def __init__(self, cloud_images, count = 16):
        self.stars = []

        for i in range(count):
            self.stars.append(cloud([random.random() *99999, random.random() *99999], random.choice(cloud_images), random.random() *0.05 + 0.05, random.random() * 0.06 + 0.02))

        self.stars.sort(key=lambda x : x.depth)

    def render(self, surf, offset = (0, 0)):
        for star in self.stars:
            star.render(surf, offset)
    
    def update(self):
        for cloud in self.clouds:
            cloud.update()