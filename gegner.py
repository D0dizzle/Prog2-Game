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
class IGegnerMain(ABC):
    @abstractclassmethod
    def zustand():
        pass

class Hindernis(IGegnerMain):
    def __init__(self):
        pass

    def zustand(self):
        pass