#Dies ist die Main-Datei, hier wird der GameLoop ausgeführt

from game import *
import pygame

game_screen = GameScreen()
while True:
    game_screen.update()
    game_screen.render()
    pygame.display.update()
    clock.tick(FPS)
