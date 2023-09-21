"""Das hier ist für verschiedene Tests gekapert, nicht wundern!
Hier gibt's ne kleine Default MainLoop, in der man Funktionen ausprobieren kann"""

import pygame as pg
import sys
import random

FPS = pg.time.Clock()

schwarz = (0, 0, 0)
weiss = (255, 255, 255)
cyan = (100, 100, 255)

screen = pg.display.set_mode(size=(300, 300))
screen.fill(cyan)

#Funktion, um Tastendruck des Spielers auszuwerten und entsprechende Aktionen auszuführen
#kommt später vermutlich als Methode in die "Player"-Klasse

def update(a):                                     #a ist die derzeitige Position des Player-Sprites
    gedrueckte_Taste = pg.key.get_pressed()            
    if gedrueckte_Taste[pg.K_UP]:                   #wir schauen: wurde Pfeiltaste nach oben gedrückt?
        a.move_ip(0, -5)                            #wenn ja: bewegen wir den Spieler um -5 Pixel nach oben
    if gedrueckte_Taste[pg.K_DOWN]:                  # hier 5 pixel nach unten
        a.move_ip(0, 5)
    if gedrueckte_Taste[pg.K_LEFT]:                 #-5 pixel nach links
        a.move_ip(-5, 0)
    if gedrueckte_Taste[pg.K_RIGHT]:                #5 pixel nach rechts
        a.move_ip(5, 0)

def exit_game():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()                       #Quelle für pygame.quit(): coderslegacy.com/python/python-pygame-tutorial
            sys.exit()


#Main Loop:
while True:

    
    exit_game()
    pg.display.update()

