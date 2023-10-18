import pygame
import os
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *


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
        self.sprite.render()


    def get_pos(self):
        self.position = (self.rect.x, self.rect.y)
        return self.position

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
