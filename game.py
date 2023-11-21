#### Datei für Kollision usw.
import pygame
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *
from enemy import *
from player import *

#### Interface und Zustand-Klassen für die verschiedenen Spiel-Abschnitte
class gameStates(ABC):
    def exit(self):
        pass

    def enter(self):
        pass

    def run(self):
        pass

class startGame(gameStates):
    pass

class playGame(gameStates):
    pass

class settings(gameStates):
    pass

class pauseGame(gameStates):
    pass

class gameOver(gameStates):
    pass


class Game:
    def __init__(self, state):
        self.state = state
    
    def update(self):
        pass

    def delete(self):
        pass

    def run(self):
        pass