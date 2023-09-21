#Autoren:   
#Titel des Spiels:

#Packages:
import pygame
import sys

#Variablen (todo: später hier drunter reinschreiben, haha)
FPS = pygame.time.Clock()
screen_hoehe = 400                  #hier setzen wir hoehe und breite des Spielfensters
screen_breite = 500
screen = pygame.display.set_mode(screen_hoehe, screen_breite)   #hier initialisieren wir das Spielfenster (erstmal ohne Grafik)

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
