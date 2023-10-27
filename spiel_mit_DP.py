#Diese Datei ist dafür da, Code in sinnvollen Design Patterns zu schreiben

import pygame
import sys
import random
import os
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *
from player import *
from gegner import *
from game import *

spieler = PlayerSprite()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(game_folder,"Assets","sounds","BGM.wav"))
pygame.mixer.music.play(-1, 0)
pygame.mixer.music.set_volume(0.4)
#hindernisCreator = HindernisCreator()
#hindernis = hindernisCreator.createHindernis()
player1 = Player1(spieler)
background = Hintergrund(hg_dict)

new_game = Game()
new_game.new()

while True:

    background.render()
    player1.update()
    player1.shoot(projectiles)


    sprites = pygame.sprite.Group(player1, projectiles, new_game.sprites)
    sprites.draw(screen)
    exit_game()
    pygame.display.update()
    FPS.tick(FPS_anzahl)