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
sprites = [spieler, projectil]
background = Hintergrund(hg_dict)
while True:
    background.update()
    exit_game()
    for sprite in sprites:
        sprite.update()

    pygame.display.update()