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

class ObstacleCreator:
    def createObstacle(self, x, y, style):
        if style == "Pilz":
            hindernis = ObstacleSatellite(x, y)
        elif style == "Cyan":
            hindernis = ObstacleCyan(x, y)
        hindernis.__init__(x, y)
        return hindernis

class ObstacleOnScreen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
    
    def new(self):
        self.map = TileMap(img_dict["TME"])
        for col, tiles in enumerate(self.map.data):
            for row, tile in enumerate(tiles):
                if tile == '1':
                    obstacleCreator = ObstacleCreator()
                    self.sprites.append(obstacleCreator.createObstacle(row * 25, (col) * 25, "Pilz"))

class MobilerGegner(IBaseGegnerMain):
    def __init__(self):
        pass

    def update(self):
        pass

    def zustand(self):
        pass

class SegmentCreator:
    def createSegment(self, x, y, seg_kind):
        if seg_kind == "head":
            segment = SegmentKopf(x, y)
        elif seg_kind == "body":
            segment = SegmentKoerper(x, y)
        segment.__init__(x, y)
        return segment


class Centipede:
    def __init__(self):
        self.segments = []
        self.length = 10

    def createCentipede(self):
        segmentCreator = SegmentCreator()
        for i in range(self.length):
            if i == 0:
                self.segments.append(segmentCreator.createSegment(i* 0, i*0, "body"))
            elif i < self.length - 1:
                self.segments.append(segmentCreator.createSegment(i* 25, i*0, "body"))
            elif i == self.length - 1:
                self.segments.append(segmentCreator.createSegment(i * 25, i * 0, "head"))