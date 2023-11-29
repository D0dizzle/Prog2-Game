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
    
    def new(self, ufo_sprites: list):
        self.map = TileMap(img_dict["TME"])
        for col, tiles in enumerate(self.map.data):
            for row, tile in enumerate(tiles):
                if tile == '1':
                    obstacleCreator = ObstacleCreator()
                    ufo_sprites.append(obstacleCreator.createObstacle(row * 25, (col) * 25, "Pilz"))

    def delete(self, ufo_sprites: list):
        for sprite in ufo_sprites:
            if sprite.isAlive == "dead":
                ufo_sprites.remove(sprite)

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
    def collide_with_border(self, seg: ISegment):
        if seg.rect.left < 0:
            seg.rect.left = 0
        seg.change_state(looksDown())
    def collide_with_obstacle(self, seg: ISegment):
        seg.change_state(looksDown())
    def exit(self, seg: ISegment):
        seg.state_before = looksLeft()

    def move(self, seg: ISegment):
        seg.rect.x -= 2  


class looksRight(segState):
    def collide_with_border(self, seg: ISegment):
        if seg.rect.right > width:
            seg.rect.right = width
        seg.change_state(looksDown())
    
    def collide_with_obstacle(self, seg: ISegment):
        seg.change_state(looksDown())

    def exit(self, seg: ISegment):
        seg.state_before = looksRight()

    def move(self, seg: ISegment):
        seg.rect.x += 2

class looksDown(segState):      #####Hier aufpassen! anderes Verhalten bei SegHead/SegBody! 
    def counter_reached(self, seg: ISegment):
        self.counter = 0
        if isinstance(seg.state_before, looksLeft):
            seg.change_state(looksRight())
            seg.counter = 0
        elif isinstance(seg.state_before, looksRight):
            seg.change_state(looksLeft())
            seg.counter = 0

    def move(self, seg: ISegment):
        seg.rect.y += 1
        seg.counter += 1
    
    def exit(self, seg: ISegment):
        seg.state_before = looksDown()
        seg.counter = 0

class SegmentKopf(pygame.sprite.Sprite, Observable, ISegment): ###Kontext im Sinne des State Patterns
    def __init__(self, x, y):
        super().__init__()
        self.obstacleCreator = ObstacleCreator()
        self.image = centipede_img_dict["Head"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.counter = 0
        self.state = looksLeft()
        self.state_before = self.state
        self.hp = 1
        self.isAlive = "alive"
        self.observers = []

    def change_state(self, newState: segState):
        if (self.state != None):
            self.state.exit(self)
        self.state = newState
        self.state.enter()


    def status(self, status_change: str, ufo_sprites: list):
        if status_change == "hit":
            self.hp -= 1
            if self.hp == 0:
                ufo_sprites.append(self.obstacleCreator.createObstacle(self.rect.x, self.rect.y, "Pilz"))
                self.isAlive = "dead"
        elif status_change == "collideWithWall" and self.counter == 0 :
            self.state.collide_with_obstacle(self)

    def move(self):
        self.state.move(self)
        if self.counter == 25:
            self.state.counter_reached(self)
        elif self.rect.x <= 0 and isinstance(self.state, looksLeft):
            self.state.collide_with_border(self)
        elif self.rect.right >= width and isinstance(self.state, looksRight):
            
            self.state.collide_with_border(self)
    
class SegmentKoerper(pygame.sprite.Sprite, Observer, ISegment):
    def __init__(self, x, y):
        super().__init__()
        self.obstacleCreator = ObstacleCreator()
        self.image = centipede_img_dict["Body"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.hp = 1
        self.isAlive = "alive"
        self.state = looksLeft()
        self.notif = False
        self.counter = 0
        self.counter2 = 0

    def notification(self, observable: Observable):
        pass

    def change_state(self, newState: segState):
        if (self.state != None):
            self.state.exit(self)
        self.state = newState
        self.state.enter()
    
    def status(self, status_change: str, ufo_sprites: list):
        if status_change == "hit":
            self.hp -= 1
            if self.hp == 0:
                ufo_sprites.append(self.obstacleCreator.createObstacle(self.rect.x, self.rect.y, "Pilz"))
                self.isAlive = "dead"

        elif status_change == "collideWithWall" and self.counter == 0 :
            self.state.collide_with_obstacle(self)

    
    def move(self):
        self.state.move(self)
        if self.counter == 25:
            self.state.counter_reached(self)
        elif self.rect.x <= 0 and isinstance(self.state, looksLeft):
            self.state.collide_with_border(self)
        elif self.rect.right >= width and isinstance(self.state, looksRight):
            
            self.state.collide_with_border(self)


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
        for i in range(10):
            if i == 0:
                self.segments.append(segmentCreator.createSegment(self.x - (25*i), i * self.y, "body"))
            elif i < 10 - 1:
                self.segments.append(segmentCreator.createSegment(self.x - (25*i), i * self.y, "body"))
            elif i == 10 - 1:
                self.segments.append(segmentCreator.createSegment(self.x - (25*i), i * self.y, "head"))

    def observer(self): 
        for segment in self.segments[:len(self.segments)-1]:
            self.segments[len(self.segments)-1].register(segment)

    def update(self):
        for segment in self.segments:
            segment.move()
            if segment.isAlive == "dead":
                self.segments.remove(segment)












###############################################################################

class MobilerGegner(IBaseGegnerMain):
    def __init__(self):
        pass

    def update(self):
        pass

    def zustand(self):
        pass
