###### File um alles rund um Gegner-Klassen zu bündeln ######
##   Mögliche Klassenarten: Main, Bewegung, Kollision    ##

#imports:
import pygame
import os
import random
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *

#Interface für Gegner Main-Klassen:
class IBaseGegnerMain(ABC):
    @abstractclassmethod
    def zustand():
        pass

class Hindernis(IBaseGegnerMain):
    def __init__(self):
        pass

    def zustand(self):
        pass

class MobilerGegner(IBaseGegnerMain):
    def __init__(self):
        pass
    def zustand(self):
        pass

class ISegment(ABC):
    @abstractclassmethod  
    def zustand(self):
        pass

class KopfSegment(ISegment):
    def __init__(self):
        pass
    def zustand(self):
        pass

class KoerperSegment(ISegment):
    def __init__(self):
        pass
    def zustand(self):
        pass