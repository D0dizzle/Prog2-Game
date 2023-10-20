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



class Player1(pygame.sprite.Sprite, iPlayer):
    def __init__(self, sprite: PlayerSprite):
        super().__init__()
        self.sprite = sprite
        self.image = self.sprite.image
        self.vx = 5
        self.vy = 5
        self.rect = self.sprite.rect
        self.position = sprite.position


    def update(self):
        self.bewegung()




    #Bewegungsfunktion muss scheinbar in Klasse (sonst Bäh), vielleicht "PlayerMovement"-Class?? ###
    def bewegung(self):
        key_press = pygame.key.get_pressed()         
        if key_press[pygame.K_UP] and self.rect.top > 450:
            self.rect.y += self.vy * -1                           #wenn ja: bewegen wir den Spieler um -5 Pixel nach oben
        if key_press[pygame.K_DOWN] and self.rect.bottom < hoehe:                     # hier 5 pixel nach unten
            self.rect.y += self.vy 
        if key_press[pygame.K_LEFT] and self.rect.left > 0:                 #-5 pixel nach links
            self.rect.x += self.vx * -1
        if key_press[pygame.K_RIGHT] and self.rect.right < breite:                #5 pixel nach rechts
            self.rect.x += self.vx 


    def zustand(self):
        pass
    
