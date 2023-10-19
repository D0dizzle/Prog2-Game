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
        self.vx = 5
        self.vy = 5
        self.rect = self.sprite.rect
        self.position = sprite.position


    def update(self):
        self.bewegung()

        self.sprite.set_pos((self.rect.x, self.rect.y))
        self.sprite.render()


    #Bewegungsfunktion muss scheinbar in Klasse (sonst Bäh), vielleicht "PlayerMovement"-Class?? ###
    def bewegung(self):
        gedrueckte_Taste = pygame.key.get_pressed()         
        if gedrueckte_Taste[pygame.K_UP] and self.rect.top > 450:
            self.rect.y += self.vy * -1                           #wenn ja: bewegen wir den Spieler um -5 Pixel nach oben
        if gedrueckte_Taste[pygame.K_DOWN] and self.rect.bottom < hoehe:                     # hier 5 pixel nach unten
            self.rect.y += self.vy 
        if gedrueckte_Taste[pygame.K_LEFT] and self.rect.left > 0:                 #-5 pixel nach links
            self.rect.x += self.vx * -1
        if gedrueckte_Taste[pygame.K_RIGHT] and self.rect.right < breite:                #5 pixel nach rechts
            self.rect.x += self.vx 


    def zustand(self):
        pass
    
    def shoot(self):
        pass

