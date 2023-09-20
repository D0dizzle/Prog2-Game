"""Das hier ist für verschiedene Tests, nicht wundern!
Hier gibt's ne kleine Default MainLoop, in der man Funktionen ausprobieren kann"""

import pygame as pg
import sys

FPS = pg.time.Clock()

schwarz = pg.color(0, 0, 0)
weiss = pg.color(255, 255, 255)

bildschirm = pg.display.set_mode(300, 300)
