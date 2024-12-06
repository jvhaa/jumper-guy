import pygame
import random

class Physics_Entity:
    def __init__(self, game, e_type, pos, size):
        self.iframes = 0
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.stun = 0
        self.anim_offset = (0,0)
        self.ogsize = size

        self.action = "idle"
        self.flip = False
        self.animation = self.game.assets[self.type + "/" + "idle"].copy()
        self.last_movement = [0, 0]
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()
            self.pos[0] -= self.anim_offset[0]
            self.pos[1] -= self.anim_offset[1]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement = (0, 0)):
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        print(self.size, self.ogsize)
        self.pos[0] += (self.size[0] - self.ogsize[0]) * (-1 if self.flip else 1)
        self.pos[1] -= (self.size[1] - self.ogsize[1])

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        self.animation.update()
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.pos = [self.pos[0], self.pos[1]]

        self.velocity[1] = min(5, self.velocity[1]+0.1)
        self.iframes = max(self.iframes-1, 0)
        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0]-0.1)
        if self.velocity[0] < 0:
            self.velocity[0] = min(0, self.velocity[0] +0.1)
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                    self.velocity[0] = 0
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                    self.velocity[0] = 0
                self.pos[0] = entity_rect.x
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        self.last_movement = movement
    
    def render(self, surf, scroll=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))

class player(Physics_Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        self.jumps = 3
        self.wall_slide = False
        self.dashing = 0
        self.hp = 100

    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement)
        self.ogsize = self.size
        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0
            self.jumps = 1
        self.wall_slide = False
        if (self.collisions['right'] or self.collisions["left"]) and self.air_time > 4:
            self.size = (12, 24)
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            self.set_action("wall_slide")
            if self.collisions['right']:
                self.flip = True
            else:
                self.flip = False

        if self.dashing > 0:
            self.dashing = max(self.dashing -1, 0)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing+1)
        if abs(self.dashing) > 20:
            self.velocity[0] = abs(self.dashing)/self.dashing*8
            if abs(self.dashing) == 21:
                self.velocity[0] *= 0.1

        if not self.wall_slide:
            if self.air_time > 4:
                pass
                #self.set_action("jump")
            elif movement[0] != 0:
                self.set_action("run")
                self.size = (16, 24)
            else:
                self.anim_offset = (0,0)
                self.size = (13, 22)
                self.set_action("idle")
    
    def render(self, surf, scroll=(0, 0)):
        super().render(surf, scroll)

    def jump(self):
        if self.wall_slide:
            if not self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.jumps = max(0, self.jumps-1)
                self.air_time = 5
                return True
            if self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.jumps = max(0, self.jumps-1)
                self.air_time = 5
                return True

        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True
        
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -30
            else:
                self.dashing = 30

class enemy(Physics_Entity):
    def __init__(self, game, pos, size, type):
        super().__init__(game, type, pos, size)
        self.type = type
        self.attack = 0
        self.speed = 1

    def update(self, tilemap):
        movement = (0,0)
        player_dist = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1]-self.pos[1])
        insight = ((self.flip and player_dist[0] < 0) or (not self.flip and player_dist[0] > 0)) and abs(player_dist[1]) < 70
        attack = (abs(player_dist[0]) < self.attack_range) and insight
        if attack:
            if not self.attack:
                self.set_action("charge")
                self.attack = self.cd + self.charge

            self.attack = max(0, self.attack-1)
            if self.attack == self.cd:
                if self.type == "skeleton_archer":
                    self.arrow()
        else:
            self.attack = 0
        
        if self.flip:
            movement[0] = -self.speed
            if not tilemap.solidcheck((self.pos[0]-self.speed, self.pos[1])):
                movement[0] = 0
                self.flip = not self.flip
        else:
            movement[0] = self.speed
            if not tilemap.solidcheck((self.pos[0]+self.speed, self.pos[1])):
                movement[0] = 0
                self.flip = not self.flip

        if random.random() > 0.995 or (self.collisions["right"] or self.collisions["left"]) and not insight:
            self.flip = not self.flip

        super().update(tilemap, movement)

    
    def render(self, surf, scroll=(0,0)):
        super().render(surf, scroll)
    
    def arrow(self):
        xdiff = (self.game.player.pos[0]-self.pos[0]+self.game.player.size[0]/2)
        ydiff = (self.game.player.pos[1]-self.pos[1]+self.game.player.size[1]/2)
        hyp = (xdiff**2 + ydiff**2) ** 0.5
        speed = (xdiff / hyp*2, ydiff / hyp*2)
        hitbox = {"pos": (self.pos[0], self.pos[1]), "vel": speed, "size": (5,5), "speed" : (speed[0]*1, speed[1]*1), "type": "enemy", "hploss": 2, "timer": 1000, "stun" : 6, "image" : self.type + "/bullet", "iframes": 20}
        self.game.hitbox.append(hitbox)


class skeleton_archer(enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos, (24, 12), "skeleton_archer")
        self.cd = random.randint(20, 100)
        self.size = (20, 20)