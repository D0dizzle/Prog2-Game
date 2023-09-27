"""Das hier ist für verschiedene Tests gekapert, nicht wundern! test test  gsg
Hier gibt's ne kleine Default MainLoop, in der man Funktionen ausprobieren kann"""

import pygame as pg
import sys
import random
import os
from abc import ABC, abstractclassmethod

from pygame.sprite import* 

pg.display.set_caption("Centipeter")
FPS = pg.time.Clock()

schwarz = (0, 0, 0)
weiss = (255, 255, 255)
cyan = (100, 100, 255)

game_folder = os.path.dirname(__file__)

screen = pg.display.set_mode(size=(500, 500))
#TODO os.path.join um os path zu verallgrmrinrtn


background1 = pg.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert()
background = pg.transform.scale(background1, (500, 500))
background2 = pg.image.load(os.path.join(game_folder,"Assets","hintergrund" ,"parallax-space-ring-planet.png")).convert_alpha()
background3 = pg.image.load(os.path.join(game_folder,"Assets","hintergrund","parallax-space-stars.png")).convert_alpha()
background4 = pg.transform.scale(background3, (500, 500))

# Background Asset Quelle: https://opengameart.org/content/space-background-3


#Funktion, um Tastendruck des Spielers auszuwerten und entsprechende Aktionen auszuführen
#kommt später vermutlich als Methode in die "Player"-Klasse

"""def update(a):                                     #a ist die derzeitige Position des Player-Sprites
    gedrueckte_Taste = pg.key.get_pressed()            
    if gedrueckte_Taste[pg.K_UP]:                   #wir schauen: wurde Pfeiltaste nach oben gedrückt?
        a.move_ip(0, -5)                            #wenn ja: bewegen wir den Spieler um -5 Pixel nach oben
    if gedrueckte_Taste[pg.K_DOWN]:                  # hier 5 pixel nach unten
        a.move_ip(0, 5)
    if gedrueckte_Taste[pg.K_LEFT]:                 #-5 pixel nach links
        a.move_ip(-5, 0)
    if gedrueckte_Taste[pg.K_RIGHT]:                #5 pixel nach rechts
        a.move_ip(5, 0)"""

def exit_game():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()                       #Quelle für pygame.quit(): coderslegacy.com/python/python-pygame-tutorial
            sys.exit()

#Klassen:
#Spieler Klasse
class player(pg.sprite.Sprite):             #Quelle für Erstellungshilfe = pygame doc
    
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y
        self.image1 = pg.image.load(os.path.join(game_folder,"Assets","ship","ship-1.png")) #Spritequelle: https://opengameart.org/content/some-top-down-spaceships
        self.image = pg.transform.scale(self.image1, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (250, 400)
        self.position = self.rect
        
    def shoot(self,vy):
        pass
    
    def update(self):
        gedrueckte_Taste = pg.key.get_pressed()         
                                    #wir schauen: wurde Pfeiltaste nach oben gedrückt?
        if gedrueckte_Taste[pg.K_UP] and self.position.y > 400:
            self.rect.move_ip(0, -1 * self.vy)                            #wenn ja: bewegen wir den Spieler um -5 Pixel nach oben
        if gedrueckte_Taste[pg.K_DOWN] and self.position.y < 450:                     # hier 5 pixel nach unten
            self.rect.move_ip(0, self.vy)
        if gedrueckte_Taste[pg.K_LEFT] and self.position.x > 0:                 #-5 pixel nach links
            self.rect.move_ip(-1 * self.vx, 0)
        if gedrueckte_Taste[pg.K_RIGHT] and self.position.x < 450:                #5 pixel nach rechts
            self.rect.move_ip(self.vx, 0)
            
class projectile(pg.sprite.Sprite):
    
    def __init__(self,x,y,vy):
        super().__init__()
        self.x = x
        self.y = y
        self.vy = vy
        self.image1 = pg.image.load(os.path.join(game_folder,"Assets","ship","Bullet2.png"))
        self.image = pg.transform.scale(self.image1, (10, 10))
        self.rect = self.image.get_rect()
        
        
        




spieler = player(20, 20, 5, 5)
spieler2 = player(20, 20, 10, 10)
#Main Loop:
while True:
    exit_game()
    spieler.update()
    spieler2.update()
    screen.blit(background, (0,0))
    screen.blit(background2, (20,50))
    screen.blit(background4, (20,50))
    screen.blit(spieler.image, spieler.position)

    pg.display.update()
    FPS.tick(60)

