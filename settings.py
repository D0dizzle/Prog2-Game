#Diese Datei ist für Settings/Einstellungen gedacht!
import pygame
import os
import sys
FPS = pygame.time.Clock()

schwarz = (0, 0, 0)
weiss = (255, 255, 255)
cyan = (100, 100, 255)

game_folder = os.path.dirname(__file__)
screen = pygame.display.set_mode(size=(500, 500))


#Funktion zum Beenden des Spiels durch "x" in der Ecke
def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                       #Quelle für pygame.quit(): coderslegacy.com/python/python-pygame-tutorial
            sys.exit()


#Hintergründe
hg_dict = {}
hg_dict["background"] = pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert()
hg_dict["space-stars"] = pygame.image.load(os.path.join(game_folder,"Assets","hintergrund" ,"parallax-space-stars.png")).convert_alpha()