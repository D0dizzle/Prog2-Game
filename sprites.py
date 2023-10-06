# Datei um alle Klassen mit Sprites zu bündeln (Spieler, Gegner, Hindernisse, Sonstiges)
# die relevanten Imports:
import pygame
import os
from abc import ABC, abstractclassmethod
from settings import *



# Klasse Sprite, damit Fehlermeldung kommt, wenn Sprite-Klasse keine Update-Methode hat
class Sprite(ABC):
    @abstractclassmethod
    def update():
        pass

#Klasse für den Player Sprite
class PlayerSprite(Sprite):
    def __init__(self, x, y, vx, vy):
        self.velx = vx
        self.vely = vy
        self.x_cord_p = x
        self.y_cord_p = y 
        self.image1 = pygame.image.load(os.path.join(game_folder,"Assets","ship","ship-1.png")) #Spritequelle: https://opengameart.org/content/some-top-down-spaceships
        self.image = pygame.transform.scale(self.image1, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (breite / 2, hoehe - hoehe / 4)
        self.position = self.rect 

    def update(self):
        screen.blit(self.image, self.position)      
