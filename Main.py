#Diese Datei ist dafür da, Code in sinnvollen Design Patterns zu schreiben

from __future__ import annotations
from settings import *
from sprites import *
from player import *
from enemy import *
from game import *
import pygame
import os
pygame.init()

pygame.mixer.init() 
pygame.mixer.music.load(os.path.join(game_folder,"Assets","sounds","BGM.wav"))
pygame.mixer.music.play(-1, 0)
pygame.mixer.music.set_volume(0.4)

player1 = Player1(player_img_dict)
background = Hintergrund(hg_dict)
new_map = ObstacleOnScreen()
new_map.new()
centipede = Centipede(10)
centipede.createCentipede()
collider = Collider()

class Score():

    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont('Corbel', 35)

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore= int(file.read())
        except FileNotFoundError:
            return 0

    def save_highscore(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.highscore))

    def update_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

    def display_scores(self):
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, white)
        score_text = self.font.render(f"Score: {self.score}", True, white)
        screen.blit(highscore_text, (10, 10))
        screen.blit(score_text, (10, 50))

    def update_score(self, enemy):
        self.score += enemy.score

highscore = Score() 

highscore.load_highscore()
highscore.update_highscore()
highscore.save_highscore()


while True:
    background.render()
    player1.update()
    player1.shoot(projectiles)
    collider.collideObstacle(projectiles, new_map.sprites)
    collider.collideObstacle(projectiles, centipede.segments)
    collider.collideWithWall(centipede.segments, new_map.sprites)
    #highscore.update_score(new_map)
    highscore.display_scores()
    new_map.delete()
    centipede.update()
    sprites = pygame.sprite.Group(player1, projectiles, new_map.sprites, centipede.segments)
    sprites.draw(screen)
    exit_game()
    pygame.display.update()
    FPS.tick(FPS_anzahl)