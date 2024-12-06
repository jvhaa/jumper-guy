import pygame
import sys
import random

from scripts.clouds import Clouds
from scripts.entity import player, enemy, skeleton_archer
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import TileMap
from scripts.button import textbox
from scripts.spark import Spark

class main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((400, 300))

        self.assets = {
            "alphabet": load_images("textsystem"),
            "clouds" : load_images("clouds"),
            "colliables": load_images("colliables"),
            "player/idle" : Animation(load_images("player/idle"), 1),
            "player/run" : Animation(load_images("player/run"), 1),
            "player/jump" : Animation(load_images("player/jump"), 1),
            "player/wall_slide" : Animation(load_images("player/wall_slide"), 1),
            "skeleton_archer/idle" : Animation(load_images("player/idle"), 1),
            "skeleton_archer/run" : Animation(load_images("player/run"), 1),
            "skeleton_archer/charge" : Animation(load_images("player/wall_slide"), 1),
        }
        
        self.clock = pygame.time.Clock()
        self.gamestate = "game"
        self.tilemap = TileMap(self, 50)
        self.level = 0
        self.clouds = Clouds(self.assets["clouds"])
        self.player = player(self, (0, 0), (12, 24))
        self.enemies = []
        self.camdiff = [0,0]
        self.move = [0, 0]
        self.load_map("0")
        self.buttons = []
        self.hitbox = []
        self.click = False

        self.b()

    def b(self):
        if self.gamestate == "title":
            self.buttons.append(textbox(self, self.display, (50, 100), "play", "game", "ho"))

        self.game_handler()

        
    def game_handler(self):
        while True:
            self.click = False
            self.mx, self.my = pygame.mouse.get_pos()
            self.mx //= 2
            self.my //= 2
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN and self.gamestate == "game":
                    if event.key == pygame.K_a:
                        self.move[0] = True
                    if event.key == pygame.K_d:
                        self.move[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_q:
                        self.player.dash()
                if event.type == pygame.KEYUP and self.gamestate == "game":
                    if event.key == pygame.K_a:
                        self.move[0] = False
                    if event.key == pygame.K_d:
                        self.move[1] = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = True
            if self.gamestate == "game":
                self.game()
            for button in self.buttons:
                button.update()
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            

    def game(self):
        self.display.fill((0, 0, 0))
        self.camdiff[0] += (self.player.rect().centerx - self.display.get_width()//2 - self.camdiff[0])//30
        self.camdiff[1] += (self.player.rect().centery - self.display.get_height()//2 -  self.camdiff[1])//30
        #self.screen.blit(self.assets["background"], (0,0))
        self.player.update(self.tilemap, (self.move[1]-self.move[0], 0))
        self.player.render(self.display, self.camdiff)
        self.tilemap.render(self.display, self.camdiff)

        for hitbox in self.hitbox.copy():
            self.hitbox[self.hitbox.index(hitbox)]["pos"] = (hitbox["pos"][0] + hitbox["vel"][0], hitbox["pos"][1] + hitbox["vel"][1])
            hit_rect = pygame.Rect(hitbox["pos"][0], hitbox["pos"][1], hitbox["size"][0], hitbox["size"][1])
            pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(hitbox["pos"][0]-self.camdiff[0], hitbox["pos"][1]-self.camdiff[1], hitbox["size"][0], hitbox["size"][1]))
            self.hitbox[self.hitbox.index(hitbox)]["timer"] -= 1
            
            if "image" in hitbox:
                self.display.blit(self.assets[hitbox["image"]], (hitbox["pos"][0]-self.camdiff[0], hitbox["pos"][1]-self.camdiff[1]))
            if hitbox["timer"] <= 0: 
                for enemies in self.enemies:
                    if "id" in hitbox:
                        if hitbox["id"] in enemies.hitboxs:
                            enemies.hitboxs.remove(hitbox["id"])
                self.hitbox.remove(hitbox)
            if hit_rect.colliderect(self.player.rect().copy()) and not self.player.iframes:
                self.player.hp -= hitbox["hploss"]
                if abs(hitbox["speed"][0]) > 1:
                    self.player.velocity[0] = hitbox["speed"][0]
                if abs(hitbox["speed"][1]) > 1:
                    self.player.velocity[1] = hitbox["speed"][1]
                self.player.iframes = max(self.player.iframes, hitbox["iframes"])
                self.hitbox.remove(hitbox)
                for i in range(4):
                    if hitbox["vel"][0] > 0:
                        self.sparks.append(Spark([self.player.rect().x, self.player.rect().centery], (random.random()*0.6 - 1)*math.pi, 3))
                    if hitbox["vel"][0] < 0:
                        self.sparks.append(Spark([self.player.rect().x+self.player.rect().width, self.player.rect().centery], (-0.5 + random.random()*0.6)*math.pi, 3))

    
    def load_map(self, map_id):
        self.tilemap.load("maps/" + str(map_id) + ".json")

        self.enemies = []
        self.sparks = []
        
        for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
            if spawner["variant"] == 0:
                self.enemies.append(skeleton_archer(self, spawner["pos"]))
        


main()