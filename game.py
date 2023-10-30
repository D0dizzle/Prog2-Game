#### Datei für Kollision usw.
import pygame
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *
from enemy import *
from player import *
"""
class Collider():
    def collideObstacle(self, spritegroup1, spritegroup2):
        for sprite2 in spritegroup2:
            for sprite1 in spritegroup1:
                if sprite2.rect.collidelist(spritegroup1) > -1:
                    sprite2.status("hit")
                    spritegroup1.remove(sprite1)"""