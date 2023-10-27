###### File um alles rund um Gegner-Klassen zu bündeln ######
##   Mögliche Klassenarten: Main, Bewegung, Kollision    ##

#imports:
import pygame
import os
import random
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *

#Interface für Gegner Main-Klassen:
class IBaseGegnerMain(ABC):
    @abstractclassmethod
    def update(self):
        pass

    @abstractclassmethod
    def zustand():
        pass

class ISegment(ABC):
    @abstractclassmethod
    def update(self):
        pass

    @abstractclassmethod  
    def zustand(self):
        pass

class HindernisCreator:
    def createHindernis(self, x, y, art):
        if art == "Pilz":
            hindernis = HindernisPilz(x, y)
        elif art == "Cyan":
            hindernis = HindernisCyan(x, y)
        hindernis.__init__(x, y)
        return hindernis

class MobilerGegner(IBaseGegnerMain):
    def __init__(self):
        pass

    def update(self):
        pass

    def zustand(self):
        pass


class KopfSegment(ISegment):
    def __init__(self, sprite: SpriteSegmentKopf):
        self.sprite = sprite
        self.rect = sprite.rect
        self.positon = self.rect

    def update(self):
        self.sprite.render()

    def zustand(self):
        pass

class KoerperSegment(ISegment):
    def __init__(self, sprite: SpriteSegmentKoerper):
        self.sprite = sprite
        self.rect = sprite.rect
        self.position = self.rect
    
    def update(self):
        self.sprite.render()

    def zustand(self):
        pass

