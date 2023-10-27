#Diese Datei ist für Settings/Einstellungen gedacht!
#### Imports:   ####
import pygame
import os
import sys
from random import randint, choice

#### Variablen: ####
black = (0, 0, 0)
white = (255, 255, 255)
cyan = (100, 100, 255)
green = (0, 255, 0)
dark_green = (100, 255, 100)
height = 1000
width = 800
FPS_anzahl = 60                     #Anzahl FPS
FPS = pygame.time.Clock()           #Pygame.time.Clock Objekt
seg_groesse = 25
projectiles = []
game_folder = os.path.dirname(__file__)
screen = pygame.display.set_mode(size=(width, height))
pygame.display.set_caption("Space Centipede")

## Hintergründe: ##
#vorab PNG's laden, die transformiert werden müssen
#background1 =  pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert()
#space_stars1 = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund" ,"parallax-space-stars.png")).convert_alpha()
#Dictionary mit den Hintergründen
hg_dict = {}
#hg_dict["background"] = pygame.transform.scale(background1, (width, height))
#hg_dict["space-stars"] = pygame.transform.scale(space_stars1, (width, height))
hg_dict["big-planet"] = {"image" : pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-big-planet.png")).convert_alpha()}
hg_dict["far-planets"] = {"image" : pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-far-planets.png")).convert_alpha()}
hg_dict["ring-planet"] = {"image" : pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-ring-planet.png")).convert_alpha()}
# hg_dict keys wird wert image zugewiesen

img_dict = {}
img_dict["bullet"] = pygame.image.load(os.path.join(game_folder,"Assets","ship","Bullet2.png"))
img_dict["satellite"] = pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "Satellite.png"))
img_dict["TME"] = os.path.join(game_folder, "Assets", "TileMapEinfach.txt")

player_img_dict = {}

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
        self.background = pygame.transform.scale(self.background, (width, height))
        self.space_stars = pygame.transform.scale(self.space_stars, (width, height))
        self.dict = dict
        self.max_particles = 500
        self.current_particles = 0
        self.last_particles = 0
        self.particles = []
        self.animated_background = [pygame.image.load(os.path.join(game_folder,"Assets","enemies" ,"particle.png")).convert_alpha(), pygame.image.load(os.path.join(game_folder,"Assets","enemies" ,"particle2.png")).convert_alpha()]
        self.cooldown = 1

        for i in self.dict:
            x = randint(50,(width-50))
            y = randint(50,(height-200))
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

        current_time = pygame.time.get_ticks()
        if current_time - self.last_particles > self.cooldown and self.current_particles < self.max_particles:
            self.last_particles = current_time                 
            self.particles.append(Particles(randint(0,width),-80, randint(2,10),choice(self.animated_background)))
            self.current_particles =+ 1
            self.cooldown = randint(0,60)

        for particle in self.particles:
            particle.update()

class Particles(pygame.sprite.Sprite):
    def __init__(self, x, y, vy, img):
        super().__init__()
        self.image = img
        self.x = x
        self.y = y
        self.vy = vy
    
    def update(self):
        screen.blit(self.image, (self.x, self.y))
        self.y += self.vy
        if self.y  < height+50:
                self.remove()


class TileMap:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'r') as f:
            for line in f:
                self.data.append(line.strip())
        self.width = len(self.data[0])
        self.height = len(self.data)