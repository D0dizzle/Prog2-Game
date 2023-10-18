import pygame
import os
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *


class iPlayer(ABC):
    @abstractclassmethod
    def update():
        pass 

    @abstractclassmethod
    def zustand():
        pass
    
    @abstractclassmethod
    def shoot():
        pass

class Spieler1(iPlayer):
    def __init__(self, sprite: PlayerSprite):
        self.sprite = sprite


    def update(self):
        self.sprite.render()
        #ToDo Bewegungsfunktion in Update-Funktion

    def zustand(self):
        pass
    
    def shoot(self):
        pass