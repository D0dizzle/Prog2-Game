#### Datei für Kollision usw.
from __future__ import annotations
import pygame
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *
from enemy import *
from player import *

background = Hintergrund(hg_dict)
player1 = Player1(player_img_dict)
new_map = ObstacleOnScreen()
new_map.new(ufo_sprites)
centipede = Centipede(10)
centipede.createCentipede()
#centipede.observer()
collider = Collider()


#### Interface und Zustand-Klassen für die verschiedenen Spiel-Abschnitte
class screenState(ABC):
    def exit(self):
        pass

    def enter(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class startScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.buttons = [
            {'rect': pygame.Rect(50, 500, 200, 50), 'text': 'Start'}, # beide hinteren Werte für die Größe
            {'rect': pygame.Rect(300, 500, 200, 50), 'text': 'Einstellungen'},
            {'rect': pygame.Rect(550, 500, 200, 50), 'text': 'Beenden'}]
        print(screen.buttons)
        screen.image = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert(),(width, height))
        
    
    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Start':
                            print("State changed")
                            screen.change_state(playScreen())
                        if button['text'] == 'Beenden':
                            pygame.quit()
                            sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()

    def render(self, screen: GameScreen):
        SCREEN.blit(screen.image, (0,0))
        for button in screen.buttons:
            rect = pygame.Rect(button['rect'])
            pygame.draw.rect(SCREEN, cyan, rect, border_radius=10)
            pygame.draw.rect(SCREEN, white, rect, width=2, border_radius=10)
            button_text = screen.font.render(button['text'], True, white)
            text_rect = button_text.get_rect(center=rect.center)
            SCREEN.blit(button_text, text_rect)
    
    def exit(self, screen: GameScreen):
        pass    

class playScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.image = background
        screen.buttons = []
    
    def update(self, screen: GameScreen):
        exit_game()
        #update der Logik
        player1.update()
        player1.shoot(projectiles)
        collider.collideObstacle(projectiles, ufo_sprites)
        collider.collideCentipede(projectiles, centipede.segments)
        collider.collideWithWall(centipede.segments, ufo_sprites)
        new_map.delete(ufo_sprites)
        centipede.update()

    def render(self, screen: GameScreen):    
        screen.image.render()
        #hier Objekte die ge"draw"ed werden sollen
        sprites = pygame.sprite.Group(player1, projectiles, ufo_sprites, centipede.segments)
        sprites.draw(SCREEN)

class settingsScreen(screenState):
    def enter(self, screen: GameScreen):
        pass
    
    def update(self, screen: GameScreen):
        pass

    def render(self, screen: GameScreen):
        pass

class pauseScreen(screenState):
    def enter(self, screen: GameScreen):
        pass
    
    def update(self, screen: GameScreen):
        pass

    def render(self, screen: GameScreen):
        pass

class gameOverScreen(screenState):
    def enter(self, screen: GameScreen):
        pass
    
    def update(self, screen: GameScreen):
        pass

    def render(self, screen: GameScreen):
        pass

class GameScreen:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(game_folder,"Assets","sounds","BGM.wav"))
        pygame.mixer.music.play(-1, 0)
        pygame.mixer.music.set_volume(0)
        self.image = None
        self.screen_state = startScreen()
        self.buttons = []
        self.screen_state.enter(self)
        self.font = pygame.font.SysFont('Corbel', 35)

    def change_state(self, newState: screenState):
        if (self.screen_state != None):
            self.screen_state.exit(self)
        self.screen_state = newState
        self.screen_state.enter(self)
    
    def render(self):
        self.screen_state.render(self)

    def update(self):
        self.screen_state.update(self)


    def run(self):
        pass