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
        self.map = TileMap(choice(list(tilemap_dict.values())))
        for col, tiles in enumerate(self.map.data):
            for row, tile in enumerate(tiles):
                if tile == '1':
                    obstacleCreator = ObstacleCreator()
                    self.sprites.append(obstacleCreator.createObstacle(row * 25, (col) * 25, "Pilz"))

    def delete(self):
        for sprite in self.sprites:
            if sprite.state == "dead":
                self.sprites.remove(sprite)


class AsteroidSprite(pygame.sprite.Sprite):
    def __init__(self, x , y , vy , vx):
        super().__init__()
        self.image = img_dict["asteroid"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vy = vy
        self.vx = vx
        if self.vx == -1:
            self.image = pygame.transform.rotate(self.image, 315)
        elif self.vx == 1:
            self.image = pygame.transform.rotate(self.image, 45)  

    def update(self):

        screen.blit(self.image,self.rect)
        self.rect.y += self.vy
        self.rect.x += self.vx

    def zustand(self):
        pass

class Asteroid():

    def __init__(self):
        self.max_asteroids = 2
        self.current_asteroids = 0
        self.last_asteroid = 0
        self.asteroidslist = []
        self.cooldown = randint(3000,5000)

    def render(self):

        creator = AsteroidCreator()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_asteroid > self.cooldown and self.current_asteroids < self.max_asteroids:
            self.last_asteroid = current_time               
            self.asteroidslist.append(creator.createAsteroid(randint(0,width),-50, randint(2,5),randint(-1,1)))
            self.cooldown = randint(5000,10000)
            
    def update(self):
        for asteroid in self.asteroidslist:
            asteroid.update()
            if asteroid.rect.y  > height+50 or asteroid.rect.x < -50 or asteroid.rect.x > width+50:
                self.asteroidslist.remove(asteroid)
                


class AsteroidCreator():

    def createAsteroid(self, x, y, vy ,vx):

        asteroid = AsteroidSprite(x, y ,vy ,vx)
        asteroid.__init__(x, y, vy ,vx)
        return asteroid
            


class SegmentKopf(pygame.sprite.Sprite, Observable):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((seg_groesse, seg_groesse))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.counter = 0
        self.dir = "left"
        self.hp = 1
        self.state = "alive"
        self.observers = []

    def status(self, status_change: str):
        if status_change == "hit":
            self.hp -= 1
            if self.hp == 0:
                obstacleCreator = ObstacleCreator()
                obstacleCreator.createObstacle(self.rect.x, self.rect.y, "Pilz")
                self.state = "dead"
        elif status_change == "collideWithWall":
            if self.dir == "left" or self.dir == "right":
                self.dir = "down"
                self.counter = 0
                self.notify()
            if self.dir == "down":
                self.dir == "left"

    def move(self):
        if self.dir == "down":
            self.rect.y += 1
            self.counter += 1
        elif self.dir == "left":
            self.rect.x -= 2
        elif self.dir == "right":
            self.rect.x += 2
    
    def direction(self):
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
            self.rect.y += 25

    
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


















"""
class Centipede:
    def __init__(self):
        self.centipedeListCreator = CentipedeListCreator()
        self.segments = self.centipedeListCreator.createCentipedeList(10)
        self.segmentCreator = SegmentCreator()


    def deleteSegment(self):
        for segment in self.segments:
            if segment.state == "dead":
                self.segments.remove(segment)"""

                    