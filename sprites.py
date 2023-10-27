# Datei um alle Klassen mit Sprites zu bündeln (Spieler, Gegner, Hindernisse, Sonstiges)
# die relevanten Imports:
import pygame
import os
from abc import ABC, abstractclassmethod
from settings import *

# Klasse Sprite, damit Fehlermeldung kommt, wenn Sprite-Klasse keine Update- und Render-Methode hat
class Sprite(ABC):
    @abstractclassmethod
    def update():
        pass


#Klasse für den Player Sprite
class PlayerSprite(pygame.sprite.Sprite, Sprite):
    def __init__(self):
        self.image1 = pygame.image.load(os.path.join(game_folder,"Assets","ship","ship-1.png")) #Spritequelle: https://opengameart.org/content/some-top-down-spaceships
        self.image = pygame.transform.scale(self.image1, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (breite / 2, hoehe - hoehe / 6)
        self.position = self.rect 
    
    def update(self):
        pass   

class Projectile(pygame.sprite.Sprite, Sprite):
    def __init__(self, x, y, vy):
        super().__init__()
        self.image1 = pygame.image.load(os.path.join(game_folder,"Assets","ship","Bullet2.png"))
        self.image = pygame.transform.scale(self.image1, (10, 10))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vy = vy
        self.rect.center = (x, y)

    
    def update(self):
        self.rect.y -= self.vy

class HindernisCyan(pygame.sprite.Sprite, Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((seg_groesse, seg_groesse))
        self.image.fill(cyan)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        screen.blit(self.image, self.rect)

class SpriteSegmentKopf(Sprite):
    def __init__(self):
        self.image = pygame.Surface((seg_groesse, seg_groesse))
        self.image.fill(gruen)
        self.rect = self.image.get_rect()

    def render(self):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

class SpriteSegmentKoerper(Sprite):
    def __init__(self):
        self.image = pygame.Surface((seg_groesse, seg_groesse))
        self.image.fill(dunkelgruen)
        self.rect = self.image.get_rect()

    def render(self):
        screen.blit(self.image, self.rect)

    def update(self):
        pass


