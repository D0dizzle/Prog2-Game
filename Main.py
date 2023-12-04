#Diese Datei ist dafür da, Code in sinnvollen Design Patterns zu schreiben

from settings import *
from sprites import *
from player import *
from enemy import *
from game import *
import pygame


game_screen = GameScreen()
while True:
    game_screen.update()
    game_screen.render()
    pygame.display.update()
    FPS.tick(FPS_anzahl)
