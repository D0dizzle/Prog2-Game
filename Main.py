#Diese Datei ist dafür da, Code in sinnvollen Design Patterns zu schreiben

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

font = pygame.font.SysFont('Corbel', 35)

class Startscreen:
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert(),(width, height))
        # Rechtecke und Texte für die Buttons, wenn wir noch weitere hinzufügen möchten, muss die ausrichtung beachtet werden.
        self.buttons = [
            {'rect': pygame.Rect(50, 500, 200, 50), 'text': 'Start'}, # beide hinteren Werte für die Größe
            {'rect': pygame.Rect(300, 500, 200, 50), 'text': 'Button 2'},
            {'rect': pygame.Rect(550, 500, 200, 50), 'text': 'Button 3'}]
        self.font = pygame.font.SysFont('Corbel', 35)
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Start':
                            status = False
                            return status
            if event.type == pygame.QUIT:
                sys.exit()
    
    def render(self):
        screen.blit(self.background, (0,0))
        for button in self.buttons:
            rect = pygame.Rect(button['rect'])
            pygame.draw.rect(screen, dark_green, rect, border_radius=10)
            pygame.draw.rect(screen, white, rect, width=2, border_radius=10)
            button_text = self.font.render(button['text'], True, white)
            text_rect = button_text.get_rect(center=rect.center)
            screen.blit(button_text, text_rect)
                
startscreen = Startscreen()
status = True

while status == True or status == None:
    startscreen.render()
    status = startscreen.update()
    pygame.display.update()
    FPS.tick(FPS_anzahl)

while True:

    background.render()
    player1.update()
    player1.shoot(projectiles)
    collider.collideObstacle(projectiles, new_map.sprites)
    collider.collideObstacle(projectiles, centipede.segments)
    collider.collideWithWall(centipede.segments, new_map.sprites)
    new_map.delete()
    centipede.update()
    sprites = pygame.sprite.Group(player1, projectiles, new_map.sprites, centipede.segments)
    sprites.draw(screen)
    exit_game()
    pygame.display.update()
    FPS.tick(FPS_anzahl)