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

class iPlayer(ABC):
    @abstractclassmethod
    def update():
        pass 

    @abstractclassmethod
    def zustand():
        pass
    
    @abstractclassmethod
    def shoot():
        pass

class iHelpFunktion(ABC):
    @abstractclassmethod
    def function():
        pass

####Hmmmm ####
"""class PlayerMovement(iHelpFunktion):
    def __init__(self, moveplayer: iPlayer):
        self.moveplayer = moveplayer

    def function(self):
        gedrueckte_Taste = pygame.key.get_pressed()         
        if gedrueckte_Taste[pygame.K_UP] and self.sprite.rect.top > 400:
            self.vy = -5                            #wenn ja: bewegen wir den Spieler um -5 Pixel nach oben
        if gedrueckte_Taste[pygame.K_DOWN] and self.sprite.rect.bottom < 450:                     # hier 5 pixel nach unten
            self.vx = 5
        if gedrueckte_Taste[pygame.K_LEFT] and self.sprite.rect.left > 0:                 #-5 pixel nach links
            self.vy = -5
        if gedrueckte_Taste[pygame.K_RIGHT] and self.sprite.rect.right < 450:                #5 pixel nach rechts
            self.vx = 5"""


class Player1(iPlayer):
    def __init__(self, sprite: PlayerSprite):
        self.sprite = sprite
        self.vx = 0
        self.vy = 0
        self.rect = self.sprite.rect
        self.position = sprite.get_pos()


    def update(self):
        self.bewegung()
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.sprite.set_pos((self.rect.x, self.rect.y))
        self.sprite.render()


    #Bewegungsfunktion muss scheinbar in Klasse (sonst Bäh), vielleicht "PlayerMovement"-Class?? ###
    def bewegung(self):
        print("ich werd grad ausgeführt")
        gedrueckte_Taste = pygame.key.get_pressed()         
        if gedrueckte_Taste[pygame.K_UP] and self.sprite.rect.top> 400:
            self.vy = -5                            #wenn ja: bewegen wir den Spieler um -5 Pixel nach oben
        if gedrueckte_Taste[pygame.K_DOWN] and self.sprite.rect.bottom < 450:                     # hier 5 pixel nach unten
            self.vx = 5
        if gedrueckte_Taste[pygame.K_LEFT] and self.sprite.rect.left > 0:                 #-5 pixel nach links
            self.vy = -5
        if gedrueckte_Taste[pygame.K_RIGHT] and self.sprite.rect.right < 450:                #5 pixel nach rechts
            self.vx = 5


    def zustand(self):
        pass
    
    def shoot(self):
        pass



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
        self.image = pygame.Surface((10, 10))
        self.image.fill(cyan)
        self.rect = self.image.get_rect()

    def render(self):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

    
