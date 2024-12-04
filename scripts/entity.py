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

        self.action = ""
        self.flip = False
        self.animation = self.game.assets[self.type + "/" + "idle"].copy()
        self.last_movement = [0, 0]
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement = (0, 0)):
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

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        self.animation.update()
    
    def render(self, surf, scroll=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0]-scroll[0]+self.anim_offset[0], self.pos[1]-scroll[1]+self.anim_offset[1]))

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
        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0
            self.jumps = 1
        self.wall_slide = False
        if (self.collisions['right'] or self.collisions["left"]) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            self.set_action("wall_slide")
            if self.collisions['right']:
                self.flip = True
            else:
                self.flip = False

        self.punching = max(self.punching -1, 0)

        if self.dashing > 0:
            self.dashing = max(self.dashing -1, 0)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing+1)
        if abs(self.dashing) > 190:
            self.velocity[0] = abs(self.dashing)/self.dashing*8
            if abs(self.dashing) == 191:
                self.velocity[0] *= 0.1

        if not self.wall_slide and self.punching <= 5:
            if self.air_time > 4:
                self.set_action("jump")
            elif movement[0] != 0:
                self.set_action("walk")
            else:
                self.set_action("idle")
    
    def render(self, surf, scroll=(0, 0)):
        if self.iframes not in [1, 2, 3, 4,6,8, 10, 13, 16, 20]:
            super().render(surf, scroll)

class enemy(Physics_Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        self.attack = 0
        self.cd = random.randint(20, 100)

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
                pass
        else:
            self.attack = 0
        super().update(tilemap, movement)

    
    def render(self, surf, scroll=(0,0)):
        super().render(surf, scroll)