'''
    spark.py

    Particle system for the game,
    used for adding the blood & spark effects.

    Functions:
        Spark(pos, angle, speed, color) -> Spark
        update() -> bool
        render(surf, offset) -> None
'''

import math
import pygame

class Spark:
    def __init__(self, pos, angle, speed, color=(255,255,255)):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.color = color

    def update(self):
        '''
            Updates the spark's position based on its angle and speed.
            slows down the spark over time this function is ran
        '''
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed
        self.speed = max(0, self.speed-0.1)
        return not self.speed

    def render(self, surf, offset=(0,0),):
        # Render the spark on the screen
        
        render_points = [
            (self.pos[0] + math.cos(self.angle)*self.speed*3-offset[0], self.pos[1] + math.sin(self.angle)*self.speed*3-offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi *0.5)*self.speed*0.5-offset[0], self.pos[1] + math.sin(self.angle+math.pi*0.5)*self.speed*0.5-offset[1]),
            (self.pos[0] + math.cos(self.angle+math.pi)*self.speed*3-offset[0], self.pos[1] + math.sin(self.angle+math.pi)*self.speed*3-offset[1]),
            (self.pos[0] + math.cos(self.angle - math.pi *0.5)*self.speed*0.5-offset[0], self.pos[1] - math.sin(self.angle+math.pi*0.5)*self.speed*0.5-offset[1])
        ]
        pygame.draw.polygon(surf, self.color, render_points)
