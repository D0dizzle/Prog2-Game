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
        self.shoot_cd = 100
        self.last_shot = 0


    def update(self):
        self.bewegung()

    #Bewegungsfunktion muss scheinbar in Klasse (sonst Bäh), vielleicht "PlayerMovement"-Class?? ###
    def bewegung(self):  
        key_press = pygame.key.get_pressed()         
        if (key_press[pygame.K_UP] or key_press[pygame.K_w]) and self.rect.top > 450:
            self.rect.y += self.vy * -1                           #wenn ja: bewegen wir den Spieler um -5 Pixel nach oben
        if (key_press[pygame.K_DOWN] or key_press[pygame.K_s]) and self.rect.bottom < hoehe:                     # hier 5 pixel nach unten
            self.rect.y += self.vy 
        if (key_press[pygame.K_LEFT] or key_press[pygame.K_a]) and self.rect.left > 0:                 #-5 pixel nach links
            self.rect.x += self.vx * -1
        if (key_press[pygame.K_RIGHT] or key_press[pygame.K_d]) and self.rect.right < breite:                #5 pixel nach rechts
            self.rect.x += self.vx 
    
    def shoot(self, projectiles: Projectile):
        
        key_press = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if key_press[pygame.K_SPACE] and current_time - self.last_shot > self.shoot_cd:
            projectiles.append(Projectile(self.rect.centerx, self.rect.centery-20, 10))
            self.last_shot = current_time

        for projectile in projectiles:
            projectile.update()
            if projectile.rect.bottom  < -5:
                projectiles.remove(projectile)

    def zustand(self):
        pass