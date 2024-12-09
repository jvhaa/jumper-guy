import pygame
import sys
import random
import math

from scripts.clouds import Clouds
from scripts.entity import player, enemy, skeleton_archer, purple_guy
from scripts.utils import load_image, load_images, Animation, load_music
from scripts.tilemap import TileMap
from scripts.button import textbox
from scripts.spark import Spark
from scripts.items import Item

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
            "player/death_1" : Animation(load_images("player/death_1"), 1),
            "player/death_collapse" : Animation(load_images("player/death_collapse"), 1),
            "skeleton_archer/idle" : Animation(load_images("skeleton_archer/idle"), 1),
            "skeleton_archer/charge" : Animation(load_images("skeleton_archer/charge"), 1),
            "enemy_soldier/idle" : Animation(load_images("enemy_soldier/idle"), 1),
            "enemy_soldier/charge" : Animation(load_images("enemy_soldier/charge"), 1),
            "enemy_soldier/attack" : Animation(load_images("enemy_soldier/attack"), 1),
            "skeleton_archer/arrow": load_image("skeleton_archer/arrow.png"),
            "titlescreen": load_image("backgroundstuff/title.png"),
            "controlscreen": load_image("backgroundstuff/controls.png"),
            "chest" : load_image("items/1.png"),
            "heal" : load_image("items/0.png"),
            "start" : load_images("start"),
            "end" : load_images("end"),
            "heart" : load_images("heart"),
            "music" : load_music("audio/"), 
            "vig": load_image("effects/vig.png")
        }
        
        self.clock = pygame.time.Clock()
        self.gamestate = "title"
        self.current_song = self.assets["music"][0]
        self.tilemap = TileMap(self, 50)
        self.level = 4
        self.clouds = Clouds(self.assets["clouds"])
        self.player = player(self, (0, 0), (12, 24))
        self.enemies = []
        self.camdiff = [0,0]
        self.move = [0, 0]
        self.buttons = []
        self.hitbox = []
        self.click = False
        self.sparks = []
        self.music_played = []
        self.music_ingame = [
            self.assets["music"][1],
            self.assets["music"][2],
            self.assets["music"][3],
            self.assets["music"][4],
            self.assets["music"][5]
        ]
        self.music_change_needed = False
        self.transiton = False
        self.trans = 400
        self.items = []
        self.counter = 0
        self.counter_music = 0
        self.dt = 0
        self.ran_death_particles = False
        self.transition_done = True
        pygame.display.set_caption("Dundun master")
        pygame.mixer.init()
        self.b()


    def b(self):
        self.buttons = []
        if self.gamestate == "menu":
            self.buttons.append(textbox(self, self.display, (100, 100), self.assets["start"]))

        if self.gamestate[:4] == "game":
            state, level = self.gamestate.split(" ")
            self.gamestate = state
            self.level = int(level)
            self.load_map(self.level)

        if self.gamestate == "end":
            self.buttons.append(textbox(self, self.display, (100, 100), self.assets["end"]))

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

            #delta time cuz i need animations
            if self.dt > 10000000:
                self.dt = 0 
                self.counter = 0
                self.counter_music = 0
            else:
                self.dt = self.dt + self.clock.get_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN and self.gamestate == "game" and not self.player.movement_blocked:
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
            elif self.gamestate == "menu":
                self.menu()
            elif self.gamestate == "controls":
                self.control_screen()
            elif self.gamestate == "end":
                self.end()
            elif self.gamestate == "death":
                self.death()

            for button in self.buttons:
                button.update()
            trans_surf = pygame.Surface(self.display.size)
            pygame.draw.circle(trans_surf, (255, 255, 255), (self.display.get_width()//2, self.display.get_height()//2), self.trans)
            trans_surf.set_colorkey((255, 255, 255))
            self.display.blit(trans_surf, (0,0))
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.size), (0,0))
            pygame.display.update()

    def title_screen(self):
        self.display.blit(self.assets["titlescreen"], (0,0))

        if pygame.mixer.get_busy() == False or self.current_song != self.assets["music"][0]:
            self.current_song = self.assets["music"][0]
            pygame.mixer.Channel(0).set_volume(0.25)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.current_song), -1, -1, 1000)

        if self.click == True:
            self.transiton = True

        if self.trans == 0:
            self.gamestate = "controls"

    def control_screen(self):
        self.display.blit(self.assets["controlscreen"], (0,0))
        self.music_change(self.assets["music"][6])
            
        if self.click == True:
            self.transiton = True
        if self.trans == 0:
            self.gamestate = "menu"
            self.b()
        
    def menu(self):
        self.display.fill((0,0, 0))
        self.music_change(self.assets["music"][7])
        self.music_played = []
        if self.trans == 0:
            self.gamestate = "game " + str(self.level)
            self.b()
    
    def end(self):
        self.display.fill((0,0,0))
        self.music_change(self.assets["music"][7])
        self.music_played = []
        if self.trans == 0:
            self.gamestate = "title"
            self.b()

    def game(self):
        if self.current_song not in self.music_ingame:
            self.music_change(random.choice(self.music_ingame)) 
        
        if self.music_change_needed:
            self.music_change_needed = False
            RandomSongShuffle = random.choice(self.music_ingame)

            RandomSongShuffleCheck = True

            while RandomSongShuffleCheck == True:
                if len(self.music_ingame) == len(self.music_played):
                    self.music_played = []
                if RandomSongShuffle != self.current_song and RandomSongShuffle not in self.music_played:
                    RandomSongShuffleCheck = False
                else:
                    RandomSongShuffle = random.choice(self.music_ingame)

            self.music_played.append(RandomSongShuffle)
            self.music_change(RandomSongShuffle, True)

        


        if self.player.pos[1] > 1000: # reset player pos past 1000 blocks down
            #self.player.pos = self.tilemap.get_player_spawn(self.level)
            self.player.hp = 0
        
        if self.player.hp == 0 or self.player.movement_blocked: # the code to determin what happens when the player dies
            self.level = 0
            if self.counter == 0:
                self.counter = self.dt # save current time
            
            self.player.movement_blocked = True
            self.player.dead = True

            self.player.set_action("death_1") # lmao dead

            if self.ran_death_particles < 100:
                for i in range(4):
                    self.ran_death_particles += 1
                    self.player.velocity = [0, 0] # stop moving the player nerd
                    self.sparks.append(Spark([self.player.rect().x, self.player.rect().centery], (random.random()*0.6 - 1)*math.pi, 2, (255, 0, 0)))
                    self.sparks.append(Spark([self.player.rect().x+self.player.rect().width, self.player.rect().centery], (-0.5 + random.random()*0.6)*math.pi, 2, (255, 0, 0)))
            
            #add timer for around 3 seconds
            if self.dt > (self.counter + 2000):
                self.player.set_action("death_collapse") # lmao dead

            if self.dt > (self.counter + 4000):
                if self.transiton == False:
                    self.display.fill((0,0, 0))
                    self.transiton = True

                if self.trans == 0:
                    self.transition_done = False
                    self.counter = 0
                    self.player.hp = 6
                    self.player.velocity = [0, 0]
                    self.player.set_action("idle")
                    self.player.movement_blocked = False
                    self.ran_death_particles = False
            

        # this code makes me want to blow up
        if self.trans == 0 :
            if self.player.dead == True or self.transition_done == False:
                self.gamestate = "game " + str(self.level)  
            else: 
                self.gamestate = "game " + str(self.level+1)
            self.b()
            

        if self.trans > 1 and self.transition_done == False:
            self.player.dead = False
            self.transition_done = True



        self.display.fill((0, 0, 0))
        self.tilemap.render(self.display, self.camdiff)
        #heart should now render on top of the map instead of under
        self.camdiff[0] += (self.player.rect().centerx - self.display.get_width()//2 - self.camdiff[0])//30
        self.camdiff[1] += (self.player.rect().centery - self.display.get_height()//2 -  self.camdiff[1])//30
        
        self.player.update(self.tilemap, (self.move[1]-self.move[0], 0))

        self.player.render(self.display, self.camdiff)

        for item in self.items:
            I_rect = item.update()
            item.render(self.camdiff)
            if I_rect.colliderect(self.player.rect()):
                item.touched()
                self.items.remove(item)

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
                for i in range(4):
                    if hitbox["speed"][0] > 0:
                        self.sparks.append(Spark([self.player.rect().x, self.player.rect().centery], (random.random()*0.6 - 1)*math.pi, 3))
                    if hitbox["speed"][0] < 0:
                        self.sparks.append(Spark([self.player.rect().x+self.player.rect().width, self.player.rect().centery], (-0.5 + random.random()*0.6)*math.pi, 3))
                self.hitbox.remove(hitbox)
                continue
            bricks = self.tilemap.physics_rects_around(hitbox["pos"])
            for brick in bricks:
                if brick.colliderect(hit_rect) and (hitbox["vel"][0] > 0 and brick.x > hitbox["pos"][0] or hitbox["vel"][0] < 0 and brick.x < hitbox["pos"][0]):
                    for i in range(4):
                        if hitbox["vel"][0] > 0:
                            self.sparks.append(Spark([hit_rect.x, hitbox["pos"][1]], (random.random()*0.6 - 1)*math.pi, 3))
                        if hitbox["vel"][0] < 0:
                            self.sparks.append(Spark([hit_rect.x+hit_rect.width, hitbox["pos"][1]], (-0.5 + random.random()*0.6)*math.pi, 3))
                    self.hitbox.remove(hitbox)
        self.display.blit(self.assets["vig"], (0,0))
        for heart in range((self.player.hp +1) // 2):
            self.display.blit(self.assets["heart"][(self.player.hp - heart*2) > 1], (15 + heart*20, 275))  

    def music_change(self, song, skip=False):   
        if self.current_song != song and skip == False:
            if self.counter_music == 0:
                self.counter_music = self.dt
            pygame.mixer.Channel(0).fadeout(900)

            if self.dt > self.counter_music + 1000:
                self.counter_music = 0
                self.current_song = song
                pygame.mixer.Channel(0).play(song, -1, -1, 1000)
        elif skip == True:
            self.current_song = song
            pygame.mixer.Channel(0).play(song, -1, -1, 1000)

    
    def load_map(self, map_id):
        e = self.tilemap.load("maps/" + str(map_id) + ".json")
        if e == "end":
            self.gamestate ="end"
            return
        self.enemies = []
        self.sparks = []
        self.items = []
        for spawner in self.tilemap.extract([("items", 0), ("items", 1)]):
            if spawner["variant"] == 0:
                self.items.append(Item(self, spawner["pos"], "heal", (10, 10), 0.25))
            if spawner["variant"] == 1:
                self.items.append(Item(self, spawner["pos"], "chest", (20, 20), 0))

        for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1), ("spawners", 2)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
            if spawner["variant"] == 1:
                self.enemies.append(skeleton_archer(self, spawner["pos"], self.level))
            if spawner["variant"] == 2:
                self.enemies.append(purple_guy(self, spawner["pos"], self.level))
        
        self.music_change_needed = True
main()