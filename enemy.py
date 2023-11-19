###### File um alles rund um Gegner-Klassen zu bündeln ######
##   Mögliche Klassenarten: Main, Bewegung, Kollision    ##

#imports:
from __future__ import annotations
import pygame
import os
import random
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *

##### Interfaces für verschiedene Sachen #####
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

class Observer(ABC):
    @abstractclassmethod
    def notification():
        pass

class Observable:
    def __init__(self):
        self.observers = []

    def register(self, follower):
        if follower not in self.observers:
            self.observers.append(follower)

    def unregister(self, follower):
        if follower in self.observers:
            self.observers.remove(follower)

    def notify(self):
        for follower in self.observers:
            follower.notification(self)       
###########################################################

class ObstacleCreator:
    def createObstacle(self, x, y, style):
        if style == "Pilz":
            hindernis = ObstacleUfo(x, y)
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

    def delete(self):
        for sprite in self.sprites:
            if sprite.state == "dead":
                self.sprites.remove(sprite)

######################################################################################

class segState(ABC):

    def exit(self):
        pass

    def enter(self):
        pass

    def move(self):
        pass

    def collide_with_obstacle(self):
        pass

    def collide_with_border(self):
        pass

    def counter_reached(self):
        pass


class looksLeft(segState):
    def collide_with_border(self, seg: SegmentKopf):
        seg.change_state(looksDown())

    def collide_with_obstacle(self, seg: SegmentKopf):
        seg.change_state(looksDown())

    def exit(self, seg: SegmentKopf):
        seg.state_before = looksLeft()

    def move(self, seg: SegmentKopf):
        seg.rect.x -= 3   


class looksRight(segState):
    def collide_with_border(self, seg: SegmentKopf):
        seg.change_state(looksDown())
    
    def collide_with_obstacle(self, seg: SegmentKopf):
        seg.change_state(looksDown())

    def exit(self, seg: SegmentKopf):
        seg.state_before = looksRight()

    def move(self, seg: SegmentKopf):
        seg.rect.x += 3
    
    


class looksDown(segState):
    def counter_reached(self, seg: SegmentKopf):
        self.counter = 0
        if isinstance(seg.state_before, looksLeft):
            seg.change_state(looksRight())
            seg.counter = 0
        elif isinstance(seg.state_before, looksRight):
            seg.change_state(looksLeft())


    def move(self, seg: SegmentKopf):
        seg.rect.y += 1
        seg.counter += 1
    
    def exit(self, seg: SegmentKopf):
        seg.counter = 0





class SegmentKopf(pygame.sprite.Sprite, Observable): ###Kontext im Sinne des State Patterns
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((seg_groesse, seg_groesse))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.counter = 0
        self.state = looksLeft()
        self.state_before = self.state
        self.hp = 1
        #self.state = "alive"
        self.observers = []

    def change_state(self, newState: segState):
        if (self.state != None):
            self.state.exit(self)
        self.state = newState
        self.state.enter()

    #def collide_with_obstacle(self):
    #    self.state.collide_with_obstacle(self)

    def status(self, status_change: str):
        if status_change == "hit":
            self.hp -= 1
            if self.hp == 0:
                obstacleCreator = ObstacleCreator()
                obstacleCreator.createObstacle(self.rect.x, self.rect.y, "Pilz")
                self.state = "dead"
        elif status_change == "collideWithWall" and self.counter == 0 :
            self.state.collide_with_obstacle(self)
            """if self.dir == "left" or self.dir == "right":
                self.dir = "down"
                self.counter = 0
                self.notify()
            if self.dir == "down":
                self.dir == "left"""



    def move(self):
        self.state.move(self)
        if self.counter == 25:
            self.state.counter_reached(self)
        elif self.rect.x <= 0 and isinstance(self.state, looksLeft):
            self.state.collide_with_border(self)
        elif self.rect.right >= width and isinstance(self.state, looksRight):
            
            self.state.collide_with_border(self)
        
        """if self.dir == "down":
            self.rect.y += 1
            self.counter += 1
        elif self.dir == "left":
            self.rect.x -= 2
        elif self.dir == "right":
            self.rect.x += 2"""
    
    def direction(self):
        pass
        """
        if self.dir == "left" and self.rect.left == 0:
            self.dir = "down"
            self.counter = 0
        elif self.dir == "right" and self.rect.right == width:
            self.dir = "down"
            self.counter = 0
        elif self.dir == "down" and self.counter >= 25 and self.rect.left > 0:
            self.dir = "left"
            self.counter = 0
        elif self.dir == "down" and self.counter >= 25 and self.rect.right < width:
            self.dir = "right"
            self.counter = 0
        elif self.dir == "down":
            self.counter = 0
            if self.rect.x < width / 2:
                self.dir = "right"
            else:
                self.dir = "left"
            self.rect.y += 25"""

    
class SegmentKoerper(pygame.sprite.Sprite, Observer):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((seg_groesse, seg_groesse))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.hp = 1
        self.state = "alive"
        self.dir = "left"
    
    def notification(self, observable: Observable):
        self.dir = observable.dir
    
    def status(self, status_change: str):
        if status_change == "hit":
            self.hp -= 1
            self.state = "divide"
    
    def move(self):
        if self.dir == "down":
            self.rect.y += 2
        elif self.dir == "left":
            self.rect.x -= 2
        elif self.dir == "right":
            self.rect += 2
    
    def direction(self):
        pass


class CentipedeListCreator:
    def createCentipedeList(self, centi_length):
        if centi_length == 10:
            self.segments = []
            self.length = centi_length

class SegmentCreator:
    def createSegment(self, x, y, seg_kind):
        if seg_kind == "head":
            segment = SegmentKopf(x, y)
        elif seg_kind == "body":
            segment = SegmentKoerper(x, y)
        segment.__init__(x, y)
        return segment

class Centipede:
    def __init__(self, centi_length):
        self.segments = []
        self.length = 10
        self.x = width
        self.y = 0

    def createCentipede(self):
        segmentCreator = SegmentCreator()
        for i in range(self.length):
            if i == 0:
                self.segments.append(segmentCreator.createSegment(i* self.x, i * self.y, "body"))
            elif i <= self.length - 1:
                self.segments.append(segmentCreator.createSegment(i* self.x, i * self.y, "head"))

    def observer(self):
        for segment in self.segments[:len(self.segments)]:
            self.segments[0].register(segment)

    def update(self):
        for segment in self.segments:
            segment.direction()
            segment.move()











###############################################################################

class MobilerGegner(IBaseGegnerMain):
    def __init__(self):
        pass

    def update(self):
        pass

    def zustand(self):
        pass
