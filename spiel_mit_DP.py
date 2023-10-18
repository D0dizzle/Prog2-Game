#Diese Datei ist dafür da, Code in sinnvollen Design Patterns zu schreiben

import pygame
import sys
import random
import os
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *


spieler = PlayerSprite()
projectil = ProjectilSprite()
background = Hintergrund(hg_dict)
#### die Liste + sprites.render um alle sprites in der Liste zu render und zu blitten
sprites = [spieler, projectil]
while True:

    #exit_game()
    background.render()
    for sprite in sprites:
        sprite.render()

    pygame.display.update()
    FPS.tick(FPS_anzahl)