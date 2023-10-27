import pygame
import sys
import random
import os
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *
from player import *
from gegner import *

class Game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
    
    def new(self):
        game_folder = os.path.dirname(__file__)
        self.map = TileMap(os.path.join(game_folder, "Assets", "TileMapEinfach.txt"))
        for col, tiles in enumerate(self.map.data):
            for row, tile in enumerate(tiles):
                if tile == '1':
                    hindernisCreator = HindernisCreator()
                    self.sprites.append(hindernisCreator.createHindernis(row * 25, (col) * 25))

    def update(self):
        for sprite in self.sprites:
            sprite.update()