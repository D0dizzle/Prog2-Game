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
        self.map = TileMap(choice(list(tilemap_dict.values())))
        for col, tiles in enumerate(self.map.data):
            for row, tile in enumerate(tiles):
                if tile == '1':
                    obstacleCreator = ObstacleCreator()
                    ufo_sprites.append(obstacleCreator.createObstacle(row * 25, (col) * 25, "Pilz"))

    def delete(self, ufo_sprites: list):
        for sprite in ufo_sprites:
            if sprite.isAlive == "dead":
                ufo_sprites.remove(sprite)


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

        SCREEN.blit(self.image,self.rect)
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
            self.cooldown = randint(500,1000)
            
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
            
class segSpriteState(ABC):
    def enter(self):
        pass

class isHead(segSpriteState):
    def enter(self, seg: ISegment):
        seg.image = centipede_img_dict["Head"]
    
    def swap_head_and_body(self, seg: ISegment):
        seg.change_sprite_state(isBody())

    def exit(self, seg: ISegment):
        seg.image = None

class isBody(segSpriteState):
    def enter(self, seg: ISegment):
        seg.image = centipede_img_dict["Body"]

    def swap_head_and_body(self, seg: ISegment):
        seg.change_spritestate(isHead())

    def exit(self, seg: ISegment):
        seg.image = None

class segState(ABC):

    def exit(self):
        pass

    def enter(self, seg: ISegment):
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

class Segment(ISegment, pygame.sprite.Sprite):
    def __init__(self, x, y, seg_sprite: segSpriteState):
        super().__init__()
        self.sprite_state = seg_sprite
        self.image = None
        self.sprite_state.enter(self)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.obstacleCreator = ObstacleCreator()
        self.counter = 0
        self.state = looksLeft()
        self.state_before = self.state
        self.hp = 1
        self.isAlive = "alive"
    
    def change_state(self, newState):
        if (self.state != None):
            self.state.exit(self)
        self.state = newState
        self.state.enter(self)

    def change_sprite_state(self, newState):
        if (self.sprite_state != None):
            self.sprite_state.exit(self)
        self.sprite_state = newState
        self.sprite_state.enter(self)

    def status(self, status_change: str, ufo_sprites: list):
        if status_change == "hit":
            self.hp -= 1
            if self.hp == 0:
                ufo_sprites.append(self.obstacleCreator.createObstacle(self.rect.x, self.rect.y, "Pilz"))
                self.isAlive = "dead"
        elif status_change == "collideWithWall" and self.counter == 0 and isinstance(self.state, looksDown) == False:
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

class Centipede:
    def __init__(self, centi_length):
        self.segments = []
        self.length = 10
        self.x = width
        self.y = 0

    def createCentipede(self):
        for i in range(10):
            if i == 0:
                self.segments.append(Segment(self.x - (25*i), i * self.y, isBody()))
            elif i < 10 - 1:
                self.segments.append(Segment(self.x - (25*i), i * self.y, isBody()))
            elif i == 10 - 1:
                self.segments.append(Segment(self.x - (25*i), i * self.y, isHead()))

    def update(self):
        i = 0
        for segment in self.segments:
            segment.move()
            if segment.isAlive == "dead":
                index = i
                if isinstance(segment.state, looksLeft):
                    index += 1
                    self.segments[index].change_sprite_state(isHead())
                    print(self.segments[index].sprite_state)
                elif isinstance(segment.state, looksRight):
                    index -= 1 
                    self.segments[index].change_sprite_state(isHead())   
                print(self.segments[index].sprite_state)
                self.segments.remove(segment)
            i += 1

###############################################################################

                    
