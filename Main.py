#Autoren:   
#Titel des Spiels:

#Packages:
import pygame
import sys

#Variablen (todo: später hier drunter reinschreiben, haha)
FPS = pygame.time.Clock()

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

    pygame.display.update()     #die Funktion macht, dass alle Änderungen im Spieler Screen angezeigt werden
    FPS.tick(60)                #60 bedeutet, dass das Spiel in 60 FPS angezeigt wird
