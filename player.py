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

class ProjectileCreator:
    def createProjectile(self,x, y, vy, proj_kind):
        if proj_kind == "basic":
            basic_projectile = Projectile(x, y, vy)
        basic_projectile.__init__(x, y, vy)
        return basic_projectile

class Player1(pygame.sprite.Sprite, iPlayer):
    def __init__(self, dict, x , y):
        super().__init__()
        self.dict = dict
        self.image = self.dict["player0"]
        self.vx = 3
        self.vy = 3
        self.ax = 0
        self.ay = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.state = "alive"
        self.shoot_cd = 200
        self.last_shot = 0
        self.shoot_sound = pygame.mixer.Sound(os.path.join(game_folder,"Assets","sounds","shoot.wav"))
        self.death_sound = pygame.mixer.Sound(os.path.join(game_folder,"Assets","sounds","death_player.ogg"))
        self.timer = 0
        self.dir = 0

    def update(self):
        self.bewegung() 
        if self.timer < 5 and self.timer > -5:
            if self.dir < -1.3:
                self.image = self.dict["player"+str(self.timer)]
                self.timer -= 1
            elif self.dir > 1.3:
                self.image = self.dict["player"+str(self.timer)]
                self.timer += 1
        elif self.dir < 1.3 and self.dir > -1.3:
            self.timer = 0
            self.image = self.dict["player"+str(self.timer)]
        #Bewegungsgleichung
        self.ax += self.vx * player_friction
        self.ay += self.vy * player_friction
        self.vx += self.ax
        self.vy += self.ay
        self.rect.x += self.vx + 0.5 * self.ax
        self.rect.y += self.vy + 0.5 * self.ay
        
    def bewegung(self):  
        self.ax = 0
        self.ay = 0
        self.dir = 0
        key_press = pygame.key.get_pressed()         
        if (key_press[pygame.K_UP] or key_press[pygame.K_w]) and self.rect.top > height*0.75:
            self.ay = -player_acc                          #wenn ja: bewegen wir den Spieler um -5 Pixel nach oben
        if (key_press[pygame.K_DOWN] or key_press[pygame.K_s]) and self.rect.bottom < height -10:                     # hier 5 pixel nach unten
            self.ay = player_acc
        if (key_press[pygame.K_LEFT] or key_press[pygame.K_a]) and self.rect.left > 10:                 #-5 pixel nach links
            self.ax = -player_acc
            self.dir = -player_acc
        if (key_press[pygame.K_RIGHT] or key_press[pygame.K_d]) and self.rect.right < width -10:                #5 pixel nach rechts
            self.ax = player_acc
            self.dir = player_acc
        if (key_press[pygame.K_RIGHT] and key_press[pygame.K_LEFT]) or (key_press[pygame.K_a] and key_press[pygame.K_s]):
            self.ax = 0
            self.dir = 0
        if self.ax != 0 and self.ay != 0:
            self.ax *= 0.7071
            self.ay *= 0.7071
    
    def shoot(self, projectiles: Projectile):
        projectileCreator = ProjectileCreator()
        key_press = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if key_press[pygame.K_SPACE] and current_time - self.last_shot > self.shoot_cd:
            projectiles.append(projectileCreator.createProjectile(self.rect.centerx, self.rect.centery-20, 10, "basic"))
            self.last_shot = current_time
            self.shoot_sound.play()
            


        for projectile in projectiles:
            projectile.update()
            if projectile.rect.bottom  < -5:
                projectiles.remove(projectile)

    def zustand(self, state:str):

        if state == "dead":
            print(state)
            self.remove()
            self.death_sound.play()
