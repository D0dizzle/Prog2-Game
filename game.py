#### Datei für Kollision usw.
from __future__ import annotations
import pygame
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *
from enemy import *
from player import *


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
        
    
    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Start':
                            screen.change_state(playScreen())
                        if button['text'] == 'Beenden':
                            pygame.quit()
                            sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()

    def render(self, screen: GameScreen):
        screen.blit(screen.image, (0,0))
        for button in screen.buttons:
            rect = pygame.Rect(button['rect'])
            pygame.draw.rect(SCREEN, cyan, rect, border_radius=10)
            pygame.draw.rect(SCREEN, white, rect, width=2, border_radius=10)
            button_text = screen.font.render(button['text'], True, white)
            text_rect = button_text.get_rect(center=rect.center)
            screen.blit(button_text, text_rect)
    
    def exit(self, screen: GameScreen):
        pass
    

class playScreen(screenState):
    def enter(self, screen: GameScreen):
        pass
    
    def update(self, screen: GameScreen):
        pass

    def render(self, screen: GameScreen):    
        pass

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
        self.image = None
        self.buttons = []
        self.screen_state = startScreen()
        self.font = pygame.font.SysFont('Corbel', 35)

    def change_state(self, newState: screenState):
        if (self.state != None):
            self.state.exit(self)
        self.state = newState
        self.state.enter()
    
    def render(self):
        self.screen_state.render(self)

    def update(self):
        self.screen_state.update(self)


    def run(self):
        pass