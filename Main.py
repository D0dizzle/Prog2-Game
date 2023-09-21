#Autoren:   
#Titel des Spiels:

#Packages:
import pygame
import sys
import random

#Variablen (todo: später hier drunter reinschreiben, haha)
#Farben:
schwarz = (255,255, 255)
weiss = (0,0,0)
rot = (255, 0, 0)
blau = (0, 255, 0)
gruen = (0, 0, 255)

FPS = pygame.time.Clock()
screen_hoehe = 700                          #hier setzen wir hoehe und breite des Spielfensters
screen_breite = 600
screen = pygame.display.set_mode(size=(screen_hoehe, screen_breite))   #hier initialisieren wir das Spielfenster (erstmal ohne Grafik)
screen.fill(gruen)              #kann man benutzen, um den Hintergrund mit irgendwas zu fuellen

#allgemeine Funktionen:
#Spiel durch "x" in der Ecke schließen
def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                       #Quelle für pygame.quit(): coderslegacy.com/python/python-pygame-tutorial
            sys.exit()



#Platz für Klassen:


#Main-Loop
while True:
    #hier kommen die Events rein, auf die unser Programm in jedem Frame reagieren soll

    exit_game()
    pygame.display.update()     #die Funktion macht, dass alle Änderungen im Spieler Screen angezeigt werden
    #screen.blit(screen, (0,0))     brauchen wir, um den Screen von alten Grafiken zu bereinigen   
    #screen.blit(player, neue position)      brauchen wir, um den Player-Sprite wieder anzuzeigen
    FPS.tick(60)                #60 bedeutet, dass das Spiel in 60 FPS angezeigt wird
