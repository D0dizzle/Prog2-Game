#Diese Datei ist dafür da, Code in sinnvollen Design Patterns zu schreiben

import pygame
import sys
import random
import os
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *
from player import *


spieler = PlayerSprite()
projectil = ProjectilSprite()
hindernis = HindernisSprite()
player1 = Player1(spieler)
background = Hintergrund(hg_dict)
#### die Liste + sprites.render um alle sprites in der Liste zu render und zu blitten
sprites = [projectil, hindernis]
while True:
    exit_game()
    background.render()
    player1.update()
    player1.bewegung()
    for sprite in sprites:
        sprite.render()

    pygame.display.update()
    FPS.tick(FPS_anzahl)