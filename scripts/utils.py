'''
    utils.py

    This file contains the asset loading system and animation functions for enemies and player.

    Functions:
        load_image(path) -> pygame.Surface
        load_images(path) -> List[pygame.Surface]
        load_audio(path) -> pygame.mixer.Sound
        load_music(path) -> List[pygame.mixer.Sound]
'''


import os
import pygame
from scripts.fileloader import path_of

BASE_IMG_LINK = "assets/"

# Load the image into memory using Pygame.image
def load_image(path):
    img = pygame.image.load(path_of(BASE_IMG_LINK + path)).convert_alpha()
    return img

# Load the images directory
def load_images(path):
    images = []
    arr = os.listdir(path_of(BASE_IMG_LINK + path))
    arr = sorted(arr, key=lambda x: int(x.split(".")[0]))
    for img_name in arr:
        images.append((load_image(path + '/' + img_name)))
    return images


# Load the audio into memory using Pygame.mixer
def load_audio(path):
    audio = pygame.mixer.Sound(path_of(BASE_IMG_LINK + path))
    return audio

# load the music directory
def load_music(path):
    music = []
    arr = os.listdir(path_of(BASE_IMG_LINK + path))
    arr = sorted(arr, key=lambda x: int(x.split(".")[0]))
    for music_name in arr:
        music.append(load_audio(path + '/' + music_name))
    return music


# Animation class for the player and enemies
class Animation:
    def __init__(self, images, img_dur = 5, loop = True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frames = 0

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)
    
    def update(self):
        if self.loop:
            self.frames = (self.frames+1) % (self.img_dur*len(self.images))
        else:
            self.frames = min(self.frames+1 , self.img_dur * len(self.images)-1)
            if self.frames >= self.img_dur * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frames/ self.img_dur)]

    def size(self):
        return self.images[int(self.frames/self.img_dur)].get_size()
        