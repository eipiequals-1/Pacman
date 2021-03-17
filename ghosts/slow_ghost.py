import pygame
from pygame.locals import *
from .enemy import Enemy

class Slow(Enemy):
    def __init__(self, pos, vel):
        super().__init__(pos, vel)
