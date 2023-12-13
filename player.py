from __future__ import annotations
import pygame
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *

# Interface für die Player Klasse
class iPlayer(ABC):
    @abstractclassmethod
    def update():
        pass 

    @abstractclassmethod
    def status():
        pass

# Factory Pattern für die Projectiles der Player Klasse
class ProjectileCreator:
    def createProjectile(self,x, y, vy, proj_kind):
        if proj_kind == "basic":
            projectile = Projectile(x, y, vy)
        elif proj_kind == "missile":
            projectile = Missile(x, y, vy)
        projectile.__init__(x, y, vy)
        return projectile

# Interface des Commands
class PlayerCommand(ABC):
    def __init__(self, player):
        self.player = player

    @abstractclassmethod
    def execute(self):
        pass

# Konkrete Command-Klassen
class PlayerMoveLeft(PlayerCommand):
    def execute(self):
        self.player.ax = -player_acc
        self.player.dir = -player_acc

class PlayerMoveRight(PlayerCommand):
    def execute(self):
        self.player.ax = player_acc
        self.player.dir = player_acc

class PlayerMoveUp(PlayerCommand):
    def execute(self):
        self.player.ay = -player_acc 

class PlayerMoveDown(PlayerCommand):
    def execute(self):
        self.player.ay = player_acc

class Player1(pygame.sprite.Sprite, iPlayer):
    def __init__(self, dict, x , y, shoot_sound, death_sound, missile_sound, life_display):
        super().__init__()
        pygame.mixer.init()
        self.dict = dict
        self.image = self.dict["player0"]
        self.vx = 3
        self.vy = 3
        self.ax = 0
        self.ay = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.state = "alive"
        self.hp = 3
        self.shoot_cd = 200
        self.missile_cd = False
        self.missile_shoot_rate = 0
        self.last_shot = 0
        self.shoot_sound = shoot_sound
        self.death_sound = death_sound
        self.missile_sound = missile_sound
        self.timer = 0
        self.dir = 0
        self.life_display = life_display

    def update(self):
        self.move() 
        # Animation des Player Sprites:
        if self.timer < 5 and self.timer > -5:
            if self.dir < -1.7:
                self.image = self.dict["player"+str(self.timer)]
                self.timer -= 1
            elif self.dir > 1.7:
                self.image = self.dict["player"+str(self.timer)]
                self.timer += 1
        elif self.dir < 1.7 and self.dir > -1.7:
            self.timer = 0
            self.image = self.dict["player"+str(self.timer)]
        # hier wird dir = 0 gesetzt, damit die nächste Animation passt
        self.dir = 0
        
    def move(self):  
        # Wenn ax und ay nicht 0 sind (also sowohl nach links/rechts als auch nach oben/unten bewegt wird),
        # muss ax und ay mit 0.7071 multipliziert werden
        if self.ax != 0 and self.ay != 0:
            self.ax *= 0.7071
            self.ay *= 0.7071
        # Bewegungsgleichung
        self.ax += self.vx * player_friction
        self.ay += self.vy * player_friction
        self.vx += self.ax
        self.vy += self.ay
        self.rect.x += self.vx + 0.5 * self.ax
        self.rect.y += self.vy + 0.5 * self.ay
        # ax und ay auf 0 setzen, damit ax/ay durch die Bewegungsgleichung nicht unendlich ansteigen.
        self.ax = 0
        self.ay = 0
    
    def shoot(self, projectiles: Projectile):
        projectileCreator = ProjectileCreator()
        key_press = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if key_press[pygame.K_SPACE] and current_time - self.last_shot > self.shoot_cd:
            projectiles.append(projectileCreator.createProjectile(self.rect.centerx, self.rect.centery-20, 10, "basic"))
            self.last_shot = current_time
            self.shoot_sound.play()
            
        if key_press[pygame.K_m] and self.missile_cd == 300:
            projectiles.append(projectileCreator.createProjectile(self.rect.centerx, self.rect.centery-20, 10, "missile"))
            self.missile_sound.play()
            self.missile_cd = 0
        elif self.missile_cd < 300:
            self.missile_cd += 1      

        for projectile in projectiles:
            projectile.update()
            if projectile.rect.bottom  < -5:
                projectiles.remove(projectile)

    def status(self, state:str):
        if state == "hit":
            self.death_sound.play()
            self.hp -= 1
            self.life_display.loseLife()
        if self.hp == 0:
            self.state = "dead"

# Generalisierte Klasse, um per Polymorphismus gleiche Key-Methoden für verschiedene Tastaturbelegungen
# zu definieren
class Controller:
    def __init__(self):
        self.left_key = {'command': None, 'button': None}
        self.right_key = {'command': None, 'button': None}
        self.up_key = {'command': None, 'button': None}
        self.down_key = {'command': None, 'button': None}

    def set_left_key(self, cmd):
        self.left_key['command'] = cmd
    
    def set_right_key(self, cmd):
        self.right_key['command'] = cmd

    def set_up_key(self, cmd):
        self.up_key['command'] = cmd
    
    def set_down_key(self, cmd):
        self.down_key['command'] = cmd
    
    def press_left_key(self):
        self.left_key['command'].execute()

    def press_right_key(self):
        self.right_key['command'].execute()

    def press_up_key(self):
        self.up_key['command'].execute()

    def press_down_key(self):
        self.down_key['command'].execute()

# Spezialisierte Klassen von Controller um die Tastenbelegung für left/right/up/down ins "_key"-Dict
# zu definieren
class ArrowKey(Controller):
    def __init__(self):
        super().__init__()
        self.left_key['button'] = pygame.K_LEFT
        self.right_key['button'] = pygame.K_RIGHT
        self.up_key['button'] = pygame.K_UP
        self.down_key['button'] = pygame.K_DOWN

class WASDKey(Controller):
    def __init__(self):
        super().__init__()
        self.left_key['button'] = pygame.K_a
        self.right_key['button'] = pygame.K_d
        self.up_key['button'] = pygame.K_w
        self.down_key['button'] = pygame.K_s

# Factory Pattern um den richtigen Controller Typ zu erstellen
class ControllerCreator():
    def createController(self, style):
        if style == "arrow":
            controller = ArrowKey()
        if style == "wasd":
            controller = WASDKey()
        controller.__init__()
        return controller