###### File um alles rund um Gegner-Klassen zu bündeln ######
##   Mögliche Klassenarten: Main, Bewegung, Kollision    ##

#imports:
from __future__ import annotations
import pygame
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *

# Interface für die einzelnen Segmente
class ISegment(ABC):
    def update(self):
        pass
   
# Factory Pattern für die Ufo-Obstacles
class ObstacleCreator:
    def createObstacle(self, x, y, style):
        if style == "Ufo":
            obstacle = ObstacleUfo(x, y)
        elif style == "Tree":
            obstacle = ObstacleTree(x, y)
        obstacle.__init__(x, y)
        return obstacle

# Klasse zum Erstellen der Ufo-Obstacles
class ObstacleOnScreen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
    
    def new(self, ufo_sprites: list, style):
        self.map = TileMap(choice(list(tilemap_dict.values())))
        for col, tiles in enumerate(self.map.data):
            for row, tile in enumerate(tiles):
                if tile == '1':
                    obstacleCreator = ObstacleCreator()
                    ufo_sprites.append(obstacleCreator.createObstacle(row * seg_size, (col) * seg_size, style))

    def delete(self, ufo_sprites: list):
        self.score = 0
        for sprite in ufo_sprites:
            if sprite.isAlive == "dead":
                self.score = 10
                ufo_sprites.remove(sprite)

# Factory Pattern für die Asteroids
class AsteroidCreator():
    def createAsteroid(self, x, y, vy ,vx):
        asteroid = AsteroidSprite(x, y ,vy ,vx)
        asteroid.__init__(x, y, vy ,vx)
        return asteroid
     
# Klasse zum Zeichnen der Asteroids
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

# Klasse zum Generieren der einzelnen Asteroid Objekte in einer Liste und zum Auslösen der 
# update-Methode der einzelnen Asteroid Objekte in der Asteroid Liste
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
                
# Interface für den Sprite State der einzelnen Segmente
class segSpriteState(ABC):
    def enter(self):
        pass

    def exit(self):
        pass

    def swap_head_and_body(self):
        pass

# Klassen für die konkreten Zustände der Sprite States
class isHead(segSpriteState):
    def enter(self, seg: ISegment):
        seg.image = centipede_img_dict["Head"]
    
    def swap_head_and_body(self, seg: ISegment):
        seg.change_sprite_state(isBody())

    def exit(self, seg: ISegment):
        pass

class isBody(segSpriteState):
    def enter(self, seg: ISegment):
        seg.image = centipede_img_dict["Body"]

    def swap_head_and_body(self, seg: ISegment):
        seg.change_sprite_state(isHead())

    def exit(self, seg: ISegment):
        pass

# Interface für den State der Segmente
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

# Klassen für die konkrete Umsetzung der States
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
        seg.rect.x -= seg.velx

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
        seg.rect.x += seg.velx

class looksDown(segState): 
    def counter_reached(self, seg: ISegment):
        if isinstance(seg.state_before, looksRight):
            seg.change_state(looksLeft())
            seg.counter = 0
        elif isinstance(seg.state_before, looksLeft):
            seg.change_state(looksRight())
            seg.counter = 0

    def move(self, seg: ISegment):
        seg.rect.y += seg.vely
        seg.counter += seg.vely
    
    def exit(self, seg: ISegment):
        seg.state_before = looksDown()
        seg.counter = 0

# Klasse für die einzelnen Segment-Objekte
class Segment(ISegment, pygame.sprite.Sprite):
    def __init__(self, x, y, seg_sprite: segSpriteState, obstacle_style):
        super().__init__()
        self.obstacle_style = obstacle_style
        self.sprite_state = seg_sprite
        self.image = None
        self.sprite_state.enter(self)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.velx = 2
        self.vely = 1
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

    def change_sprite_state(self, newSpriteState):
        if (self.sprite_state != None):
            self.sprite_state.exit(self)
        self.sprite_state = newSpriteState
        self.sprite_state.enter(self)

    def status(self, status_change: str, ufo_sprites: list):
        if status_change == "hit":
            self.hp -= 1
            if self.hp == 0:
                ufo_sprites.append(self.obstacleCreator.createObstacle(self.rect.x, self.rect.y, self.obstacle_style))
                self.isAlive = "dead"
        elif status_change == "collideWithWall" and self.counter == 0 and isinstance(self.state, looksDown) == False:
            self.state.collide_with_obstacle(self)

    def move(self):
        self.state.move(self)
        if self.counter == seg_size:
            self.state.counter_reached(self)
        elif self.rect.x <= 0 and isinstance(self.state, looksLeft):
            self.state.collide_with_border(self)
        elif self.rect.right >= width and isinstance(self.state, looksRight):
            self.state.collide_with_border(self)

# Klasse für den ganzen Centipede (Liste von Segment Objekten)
class Centipede:
    def __init__(self):
        self.segments = []
        self.length = 10
        self.x = width
        self.y = 0
        self.score = 0

    def createCentipede(self, obstacle_style):
        for i in range(10):
            if i == 0:
                self.segments.append(Segment(self.x - (seg_size*i), i * self.y, isBody(), obstacle_style))
            elif i < 10 - 1:
                self.segments.append(Segment(self.x - (seg_size*i), i * self.y, isBody(), obstacle_style))
            elif i == 10 - 1:
                self.segments.append(Segment(self.x - (seg_size*i), i * self.y, isHead(), obstacle_style))

    def update(self):
        self.score = 0
        for index, segment in enumerate(self.segments):
            segment.move()
            if segment.isAlive == "dead":
                if index + 2 < len(self.segments) or index - 1 >= 0:
                    if isinstance(segment.state, looksLeft):
                        segment_after = self.segments[index - 1]
                        segment_after.change_sprite_state(isHead())
                    elif isinstance(segment.state, looksRight):
                        segment_before = self.segments[index + 1]
                        segment_before.change_sprite_state(isHead())
                    elif isinstance(segment.state, looksDown):
                        segment_after = self.segments[index - 1]
                        segment_after.change_sprite_state(isHead())
                self.segments.remove(segment)
                self.score = 10