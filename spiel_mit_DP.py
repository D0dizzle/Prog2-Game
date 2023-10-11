#Diese Datei ist dafür da, Code in sinnvollen Design Patterns zu schreiben

import pygame
import sys
import random
import os
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *


spieler = PlayerSprite()
projectil = ProjectilSprite(10, 10, 5)

while True:
    Hintergrund.update()
    exit_game()
    spieler.update()
    projectil.update()

    pygame.display.update()