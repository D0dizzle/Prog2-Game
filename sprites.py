# Datei um alle Klassen mit Sprites zu bündeln (Spieler, Gegner, Hindernisse, Sonstiges)
# die relevanten Imports:
import pygame
import os
from abc import ABC, abstractclassmethod
from settings import *



# Klasse Sprite, damit Fehlermeldung kommt, wenn Sprite-Klasse keine Update- und Render-Methode hat
class Sprite(ABC):
    @abstractclassmethod
    def update():           #Platz um Sprite Logik zu implementieren
        pass
    @abstractclassmethod
    def render():           #Funktion zum Rendern von Sprites 
        pass

#Klasse für den Player Sprite
class PlayerSprite(Sprite):
    def __init__(self):
        self.image1 = pygame.image.load(os.path.join(game_folder,"Assets","ship","ship-1.png")) #Spritequelle: https://opengameart.org/content/some-top-down-spaceships
        self.image = pygame.transform.scale(self.image1, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (breite / 2, hoehe - hoehe / 4)
        self.position = self.rect 

    def get_pos(self):
        return self.position
    
    def update(self):
        pass   
    
    def set_pos(self, x):
        self.position = x

    def render(self):
        screen.blit(self.image, self.position) #### hier überlegen: wie übergeben wir Position aus der Bewegungsfunktion


class ProjectilSprite(Sprite):
    def __init__(self):
        self.image1 = pygame.image.load(os.path.join(game_folder,"Assets","ship","Bullet2.png"))
        self.image = pygame.transform.scale(self.image1, (10, 10))
        self.rect = self.image.get_rect()


    def render(self):
        screen.blit(self.image, self.rect)
    
    def update(self):
        pass

class HindernisSprite(Sprite):
    def __init__(self):
        self.image = pygame.Surface((hin_groesse, hin_groesse))
        self.image.fill(cyan)
        self.rect = self.image.get_rect()

    def render(self):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

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

#TileMap, um "ersten" Zustand der "Verteilung" der Hindernisse zu definieren
class TileMap():
    def __init__(self):
        pass
    
    def read_map(self):
        #TileMap hier aus Texteditor einlesen lassen
        pass
    
    def make_map(self, sprite: HindernisSprite):
        #hier Map aus Hindernis-Sprites erstellen
        pass
