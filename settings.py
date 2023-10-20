#Diese Datei ist für Settings/Einstellungen gedacht!
#### Imports:   ####
import pygame
import os
import sys


#### Variablen: ####
schwarz = (0, 0, 0)
weiss = (255, 255, 255)
cyan = (100, 100, 255)
gruen = (0, 255, 0)
dunkelgruen = (100, 255, 100)
hoehe = 600
breite = 800
FPS_anzahl = 60                     #Anzahl FPS
FPS = pygame.time.Clock()           #Pygame.time.Clock Objekt
seg_groesse = 20
hin_groesse = 10
projectiles = []


game_folder = os.path.dirname(__file__)
screen = pygame.display.set_mode(size=(breite, hoehe))

## Hintergründe: ##
#vorab PNG's laden, die transformiert werden müssen
background1 =  pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert()
space_stars1 = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund" ,"parallax-space-stars.png")).convert_alpha()
#Dictionary mit den Hintergründen
hg_dict = {}
hg_dict["background"] = pygame.transform.scale(background1, (breite, hoehe))
hg_dict["space-stars"] = pygame.transform.scale(space_stars1, (breite, hoehe))
hg_dict["big-planet"] = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-big-planet.png")).convert_alpha()
hg_dict["far-planets"] = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-far-planets.png")).convert_alpha()
hg_dict["ring-planet"] = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-ring-planet.png")).convert_alpha()

#ToDo überlegen, wie man einen Ordner direkt in ein Dict einliest


#### Funktionen: ####
#Funktion zum Beenden des Spiels durch "x" in der Ecke
def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                       #Quelle für pygame.quit(): coderslegacy.com/python/python-pygame-tutorial
            sys.exit()


#### Klassen für Settings: ####
class Hintergrund():      #ToDo: Dict als Parameter übergeben und im Konstruktor mit self.hg_dict festlegen
    def __init__(self, dict):
        self.dict = dict
    def render(self):
        x = 0
        for i in self.dict:
            screen.blit(self.dict[i], (x /breite, x / hoehe))
            x += 30000  
            ####TODO: x += __ festlegen, damit sich unsere Background-Assets cool auf dem Hintergrund verteilen!

