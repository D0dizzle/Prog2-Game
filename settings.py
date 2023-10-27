#Diese Datei ist für Settings/Einstellungen gedacht!
#### Imports:   ####
import pygame
import os
import sys
from random import randint

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
seg_groesse = 25
projectiles = []
game_folder = os.path.dirname(__file__)
screen = pygame.display.set_mode(size=(breite, hoehe))

## Hintergründe: ##
#vorab PNG's laden, die transformiert werden müssen
#background1 =  pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert()
#space_stars1 = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund" ,"parallax-space-stars.png")).convert_alpha()
#Dictionary mit den Hintergründen
hg_dict = {}
#hg_dict["background"] = pygame.transform.scale(background1, (breite, hoehe))
#hg_dict["space-stars"] = pygame.transform.scale(space_stars1, (breite, hoehe))
hg_dict["big-planet"] = {"image" : pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-big-planet.png")).convert_alpha()}
hg_dict["far-planets"] = {"image" : pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-far-planets.png")).convert_alpha()}
hg_dict["ring-planet"] = {"image" : pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-ring-planet.png")).convert_alpha()}
# hg_dict keys wird wert image zugewiesen

#img_dict = {}

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
        self.background = pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert()
        self.space_stars = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund" ,"parallax-space-stars.png")).convert_alpha()
        self.background = pygame.transform.scale(self.background, (breite, hoehe))
        self.space_stars = pygame.transform.scale(self.space_stars, (breite, hoehe))
        self.dict = dict

        for i in self.dict:
            x = randint(50,(breite-50))
            y = randint(50,(hoehe-200))
            dict[i]["x"] = x
            dict[i]["y"] = y
            #verschachtes dict: jedem background asset key wird ein weiteres dict hinzugefügt für die werte image, x und y
            # sieht so aus: 
            # {'big-planet': {'image': <Surface(88x87x32 SW)>, 'x': 268, 'y': 124},
            #  'far-planets': {'image': <Surface(272x160x32 SW)>, 'x': 592, 'y': 387},
            #  'ring-planet': {'image': <Surface(51x115x32 SW)>, 'x': 337, 'y': 68}}

    def render(self):
        screen.blit(self.background,(0,0))
        screen.blit(self.space_stars,(0,0))


        for i in self.dict:
            screen.blit(self.dict[i]["image"], (self.dict[i]["x"],self.dict[i]["y"]))

