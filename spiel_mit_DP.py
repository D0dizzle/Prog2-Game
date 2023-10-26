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

spieler = PlayerSprite()

hindernisCreator = HindernisCreator()
hindernis = hindernisCreator.createHindernis()
player1 = Player1(spieler)
background = Hintergrund(hg_dict)

"""
def shoot(player1, projectiles, cooldown = False):
    for projectile in projectiles:
        projectile.update()
        if projectile.rect.bottom  < -5:
            projectiles.remove(projectile)
    keypress = pygame.key.get_pressed()
    if keypress[pygame.K_SPACE] and cooldown is False:
        projectiles.append(Projectile(player1.rect.centerx, player1.rect.centery-20, 10))
        cooldown = True

    if not keypress[pygame.K_SPACE]:
        cooldown = False
"""

while True:
    exit_game()
    background.render()
    player1.update()
    player1.shoot(projectiles)


    sprites = pygame.sprite.Group(player1, projectiles, hindernis)
    sprites.draw(screen)

    pygame.display.update()
    FPS.tick(FPS_anzahl)