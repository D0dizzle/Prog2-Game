#Diese Datei ist für Settings/Einstellungen gedacht!
import pygame
import os
import sys
FPS = pygame.time.Clock()

schwarz = (0, 0, 0)
weiss = (255, 255, 255)
cyan = (100, 100, 255)

game_folder = os.path.dirname(__file__)
screen = pygame.display.set_mode(size=(1000, 1000))


#Funktion zum Beenden des Spiels durch "x" in der Ecke
def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                       #Quelle für pygame.quit(): coderslegacy.com/python/python-pygame-tutorial
            sys.exit()


#Hintergründe WARNUNG! 
#vorab PNG's laden, die transformiert werden müssen
background1 =  pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert()
space_stars1 = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund" ,"parallax-space-stars.png")).convert_alpha()
#Dictionary mit den Hintergründen
hg_dict = {}
hg_dict["background"] = pygame.transform.scale(background1, (1000,1000))
hg_dict["space-stars"] = pygame.transform.scale(space_stars1, (1000, 1000))
hg_dict["big-planet"] = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-big-planet.png")).convert_alpha()
hg_dict["far-planets"] = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-far-planets.png")).convert_alpha()
hg_dict["ring-planet"] = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-ring-planet.png")).convert_alpha()

class Hintergrund:
    def update():
        for i in hg_dict:
            screen.blit(hg_dict[i], (0, 0))

