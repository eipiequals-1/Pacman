import pygame
from pygame.locals import *
from .enemy import Enemy

class Speedy(Enemy):
    def __init__(self, pos, vel):
        super().__init__(pos, vel)

    def draw(self, surface):
        super().draw(surface)

    def update(self, surface, maze):
        super().update(surface, maze)

    
