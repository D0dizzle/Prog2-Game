# Datei um alle Klassen mit Sprites zu bündeln (Spieler, Gegner, Hindernisse, Sonstiges)
# die relevanten Imports:
import pygame
from random import choice

from settings import *

# Klasse für die einzelnen Projectile Objekte 
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

# Klasse für das Missile Objekt
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, vy):
        super().__init__()
        self.image1 = img_dict["Missile"]
        self.image = pygame.transform.scale(self.image1, (20, 45))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vy = vy
        self.rect.center = (x,y)

    def update(self):
        self.rect.y -= self.vy

# Klasse für das Ufo-Obstacle Objekt
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

# Klasse für das Tree-Obstacle Objekt
class ObstacleTree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.hp = 4
        self.image = tree_img_dict["tree"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isAlive = "alive"

    def status(self, status_change: str):
        if status_change == "hit":
            self.hp -= 1
            if self.hp == -1:
                self.hp = 0
            self.image = tree_animation_dict["tree"+ str(self.hp)]
        if self.hp == 0:
            self.isAlive = "dead"