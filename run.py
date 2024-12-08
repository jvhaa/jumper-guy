import pygame
import sys
import random
import math

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
            "noncolliables" : load_images("noncolliables"),
            "player/idle" : Animation(load_images("player/idle"), 1),
            "player/run" : Animation(load_images("player/run"), 1),
            "player/jump" : Animation(load_images("player/jump"), 1),
            "player/wall_slide" : Animation(load_images("player/wall_slide"), 1),
            "skeleton_archer/idle" : Animation(load_images("skeleton_archer/idle"), 1),
            "skeleton_archer/run" : Animation(load_images("skeleton_archer/idle"), 1),
            "skeleton_archer/charge" : Animation(load_images("skeleton_archer/charge"), 1),
            "skeleton_archer/arrow": load_image("skeleton_archer/arrow.png"),
            "titlescreen": load_image("backgroundstuff/title.png"),

        }
        
        self.clock = pygame.time.Clock()
        self.gamestate = "title"
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
        self.sparks = []
        self.transiton = False
        self.trans = 400

        self.b()

    def b(self):
        if self.gamestate == "title":
            pass

        if self.gamestate[:4] == "game":
            state, level = self.gamestate.split(" ")
            self.gamestate = state
            self.level = int(level)
            self.load_map(self.level)

        self.game_handler()

        
    def game_handler(self):
        while True:
            self.trans = min(400, self.trans+3)
            if self.transiton == True:
                self.trans = max(0, self.trans-10)
            if self.trans == 0:
                self.transiton = False
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
            elif self.gamestate == "title":
                self.title_screen()
            for button in self.buttons:
                button.update()
            
            trans_surf = pygame.Surface(self.display.size)
            pygame.draw.circle(trans_surf, (255, 255, 255), (self.display.get_width()//2, self.display.get_height()//2), self.trans)
            trans_surf.set_colorkey((255, 255, 255))
            self.display.blit(trans_surf, (0,0))
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()

    def title_screen(self):
        self.display.blit(self.assets["titlescreen"], (0,0))
        if self.click == True:
            self.transiton = True

        if self.trans == 0:
            self.gamestate = "game 0"
            self.b()

    def game(self):
        self.display.fill((0, 0, 0))
        self.tilemap.render(self.display, self.camdiff)
        self.camdiff[0] += (self.player.rect().centerx - self.display.get_width()//2 - self.camdiff[0])//30
        self.camdiff[1] += (self.player.rect().centery - self.display.get_height()//2 -  self.camdiff[1])//30
        self.player.update(self.tilemap, (self.move[1]-self.move[0], 0))
        self.player.render(self.display, self.camdiff)
        for enemy in self.enemies:
            enemy.update(self.tilemap)
            enemy.render(self.display, self.camdiff)

        for spark in self.sparks.copy():
            kill = spark.update()
            spark.render(self.display, self.camdiff)
            if kill:
                self.sparks.remove(spark)

        for hitbox in self.hitbox.copy():
            self.hitbox[self.hitbox.index(hitbox)]["pos"] = (hitbox["pos"][0] + hitbox["vel"][0], hitbox["pos"][1] + hitbox["vel"][1])
            hit_rect = pygame.Rect(hitbox["pos"][0], hitbox["pos"][1], hitbox["size"][0], hitbox["size"][1])
            pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(hitbox["pos"][0]-self.camdiff[0], hitbox["pos"][1]-self.camdiff[1], hitbox["size"][0], hitbox["size"][1]))
            self.hitbox[self.hitbox.index(hitbox)]["timer"] -= 1
            
            if "image" in hitbox:
                self.display.blit(hitbox["image"], (hitbox["pos"][0]-self.camdiff[0], hitbox["pos"][1]-self.camdiff[1]))
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
            bricks = self.tilemap.physics_rects_around(hitbox["pos"])
            for brick in bricks:
                if brick.colliderect(hit_rect) and (hitbox["vel"][0] > 0 and brick.x > hitbox["pos"][0] or hitbox["vel"][0] < 0 and brick.x < hitbox["pos"][0]):
                    for i in range(4):
                        if hitbox["vel"][0] > 0:
                            self.sparks.append(Spark([hit_rect.x, hitbox["pos"][1]], (random.random()*0.6 - 1)*math.pi, 3))
                        if hitbox["vel"][0] < 0:
                            self.sparks.append(Spark([hit_rect.x+hit_rect.width, hitbox["pos"][1]], (-0.5 + random.random()*0.6)*math.pi, 3))
                    self.hitbox.remove(hitbox)

    
    def load_map(self, map_id):
        self.tilemap.load("maps/" + str(map_id) + ".json")

        self.enemies = []
        self.sparks = []
        
        for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
            if spawner["variant"] == 1:
                self.enemies.append(skeleton_archer(self, spawner["pos"], self.level))
        


main()