#Diese Datei ist dafür da, Code in sinnvollen Design Patterns zu schreiben

import pygame
import os
from settings import *
from sprites import *
from player import *
from enemy import *
from game import *


pygame.mixer.init() 
pygame.mixer.music.load(os.path.join(game_folder,"Assets","sounds","BGM.wav"))
pygame.mixer.music.play(-1, 0)
pygame.mixer.music.set_volume(0.4)

player1 = Player1(player_img_dict)
background = Hintergrund(hg_dict)
new_map = ObstacleOnScreen()
new_map.new()
centipede = Centipede()
centipede.createCentipede()
collider = Collider()

while True:

    background.render()
    player1.update()
    player1.shoot(projectiles)
    collider.collideObstacle(projectiles, new_map.sprites) 
    new_map.delete()
    sprites = pygame.sprite.Group(player1, projectiles, new_map.sprites, centipede.segments)
    sprites.draw(screen)
    exit_game()
    pygame.display.update()
    FPS.tick(FPS_anzahl)