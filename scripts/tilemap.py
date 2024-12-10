'''
    tilemap.py

    Basically the grid and collsion system for the game
    loads and renders the JSON map files.
    Plus additional functions, like getting current map player spawn point.

    Functions:
        TileMap(game, tilesize) -> TileMap
        extract(id_pairs, keep) -> list
        solid_check(pos) -> str
        tiles_around(pos) -> list
        physics_rects_around(pos) -> list
        save(path) -> None
        load(path) -> str
        get_player_spawn(map_id) -> list
        render(surf, scroll) -> None
'''


import pygame
import json
from scripts.fileloader import path_of

NEIGBOUR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (0, 0), (0,-2)]
PHYSICS_TILE = {"colliables"} # Set the tiles that are solid and can be collided with

class TileMap:
    def __init__(self, game, tilesize = 50):

        self.game = game # Game function from run.py
        self.tilesize = tilesize # Size of the tiles, 50x50 image is the default
        self.tilemap = {}   # Tiles that are on the grid system, collidable if in PHYSICS_TILE
        self.offgrid_tiles = [] # Tiles that are not on the grid system, non-collidable
    


    # Extract the tiles from the map JSON file
    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
        
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                matches[-1]["pos"] = matches[-1]["pos"].copy()
                matches[-1]["pos"][0] *= self.tilesize
                matches[-1]["pos"][1] *= self.tilesize
                if not keep:
                    del self.tilemap[loc]
        return matches
    


    # Check if the tile is solid using the X,Y position from the loaded map JSON file.
    def solid_check(self, pos):
        tile_loc = str(int(pos[0]//self.tilesize)) + ";" + str(int(pos[1]//self.tilesize)) 
        
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]["type"] in PHYSICS_TILE:
                return self.tilemap[tile_loc]["type"] # RETURNS COLLIDABLE



    # Get the tiles around the player
    def tiles_around(self, pos):
        tiles = [] #
        tile_loc = (int(pos[0]//self.tilesize), int(pos[1]//self.tilesize))
        for offset in NEIGBOUR_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1]) 
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    


    # Get the physics rects around the player
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILE:
                rects.append(pygame.Rect(tile["pos"][0] *self.tilesize, tile["pos"][1] * self.tilesize, self.tilesize, self.tilesize))
        return rects
    


    # Save the map JSON file
    def save(self, path):
        f = open(path_of(path), "w")
        json.dump({"tilemap": self.tilemap, "tilesize":self.tilesize, "offgrid_tiles":self.offgrid_tiles}, f)
        f.close()



    # Load the map JSON file
    def load(self, path):
        try:
            f = open(path_of(path), "r")
        except FileNotFoundError:
            return "end"
        world = json.load(f)
        f.close()
        self.tilemap = world["tilemap"]
        self.tilesize = world["tilesize"]
        self.offgrid_tiles = world["offgrid_tiles"]



    # Get the player spawn point from the map JSON file
    def get_player_spawn(self, map_id):
        try:
            f = open(path_of("maps/" + str(map_id) + ".json"), "r")
        except FileNotFoundError:
            return "end"
        world = json.load(f)
        f.close()

        for loc in world["offgrid_tiles"]:
            if loc["type"] == "spawners" and loc["variant"] == 0:
                return loc["pos"]



    # Renders all the tiles/images in the map
    def render(self, surf, scroll = (0, 0)):
        for x in range(scroll[0]//self.tilesize, (scroll[0] + surf.get_width())//self.tilesize+1):
            for y in range(scroll[1]//self.tilesize, (scroll[1] + surf.get_height())//self.tilesize+1):

                # Render the tiles on grid tiles
                loc = str(x) + ";" + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile["type"]][tile["variant"]], (tile['pos'][0]* self.tilesize-scroll[0], tile['pos'][1] *self.tilesize-scroll[1]))
        
        # Render the offgrid tiles
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile["type"]][tile["variant"]], (tile['pos'][0]-scroll[0], tile['pos'][1] -scroll[1]))
       
