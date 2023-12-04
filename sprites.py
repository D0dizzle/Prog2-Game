# Datei um alle Klassen mit Sprites zu bündeln (Spieler, Gegner, Hindernisse, Sonstiges)
# die relevanten Imports:
import pygame
import os
from abc import ABC, abstractclassmethod

#from pygame.sprite import _Group
from settings import *
from random import choice

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vy):
        super().__init__()
        self.image1 = img_dict["bullet"]
        self.image = pygame.transform.scale(self.image1, (10, 10))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vy = vy
        self.rect.center = (x, y)
        

    def update(self):
        self.rect.y -= self.vy

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, vy):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "rock.green-crystals.png")), (15, 25))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vy = vy
        self.rect.center = (x,y)

    def update(self):
        self.rect.y -= self.vy

class ObstacleCyan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((seg_groesse, seg_groesse))
        self.image.fill(cyan)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class ObstacleUfo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.hp = 4        
        self.image = choice(list(ufo_img_dict.values()))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isAlive = "alive"

    def status(self, status_change: str):
        if status_change == "hit":
            self.hp -= 1
            if self.hp == -1:
                self.hp = 0
            self.image = ufo_animation_dict["ufo"+ str(self.hp)]
        if self.hp == 0:
            self.isAlive = "dead"

