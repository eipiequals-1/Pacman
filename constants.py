import pygame
from pygame.locals import *

BOTTOM_BUFFER = 50
WIDTH, HEIGHT = 900, 900 + BOTTOM_BUFFER
ROWS, COLS = 30, 30
CELL_W = WIDTH // ROWS
CELL_H = (HEIGHT - BOTTOM_BUFFER) // COLS

# Colors
RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

FPS = 120

VEC = pygame.math.Vector2
PLAYER_START_POS = VEC(3, 1)
SCORE = 0

LEVELS = [
    # LEVEL 1
    ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
     "W             WW             W",
     "W WWWW WWWWWW WW WWWWWW WWWW W",
     "W WSSW WSSSSW WW WSSSSW WSSW W",
     "W WWWW WWWWWW WW WWWWWW WWWW W",
     "W                            W",
     "W WWWW WWW WWWWWWWW WWW WWWW W",
     "W WWWW WWW WWWWWWWW WWW WWWW W",
     "W       WW    WW    WW       W",
     "WWWWWWW WWWWW WW WWWWW WWWWWWW",
     "SSSSSSW WWWWW WW WWWWW WSSSSSS",
     "SSSSSSW WW          WW WSSSSSS",
     "SSSSSSW WW WWW  WWW WW WSSSSSS",
     "SSSSSSW    W  E   W    WSSSSSS",
     "SSSSSSW WW W E  E W WW WSSSSSS",
     "SSSSSSW WW WWWWWWWW WW WSSSSSS",
     "SSSSSSW WW          WW WSSSSSS",
     "SSSSSSW WW WWWWWWWW WW WSSSSSS",
     "WWWWWWW WW WWWWWWWW WW WWWWWWW",
     "W             WW             W",
     "W WWWWW WWWWW WW WWWWW WWWWW W",
     "W WWWWW WWWWW WW WWWWW WWWWW W",
     "W   WWW                WWW   W",
     "WWW WWW WW WWWWWWWW WW WWW WWW",
     "W       WW    WW    WW       W",
     "W WWWWWWWWWW WWWW WWWWWWWWWW W",
     "W                            W",
     "WWWWWWW WWWW WWWW WWWW WWWWWWW",
     "W                            W",
     "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"],

    # LEVEL 2
    ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
     "W        W          W        W",
     "W WWWWWW WWWW WW WWWW WWWWW WW",
     "W WSSSSW WSSW         WSSSW WW",
     "W WWWWWW WWWW WWWWWWWWWWWWW WW",
     "W             W              W",
     "W WWWW WWW WWWWWWWW WWW WWWW W",
     "W WWWW WWW WWWWWWWW WWW WWWW W",
     "W       WW    WW    WW       W",
     "W WWWWW WWWWW WW WWWWW WWWWWWW",
     "W WWWWW WWWWW WW             W",
     "W WW          WW WWWWWWWWWWW W",
     "W WW WWW W WW WW             W",
     "W    WWW W WW    WWWWWWWWWWW W",
     "W WW       WW WW W W E EE    W",
     "W WW WWW WWWW WW W WWWWWWWWW W",
     "W WW          WW W WWWWWWWWW W",
     "W WWWWWWWWWWW WW W           W",
     "W WWWWWWWWWWW WW W WWW WWWWW W",
     "W             WW             W",
     "W WWWWW WWWWW WW WWWWW WWWWW W",
     "W WWWSW WWWWW WW WWWWW WSWWW W",
     "W   WSW                WSW   W",
     "WWW WWW WW WWWWWWWW WW WWW WWW",
     "W       WW          WW       W",
     "W WWWWWWWWWW W W WWWWWWWWWWW W",
     "W        WSW W               W",
     "W WWWW WWWWW WWW WWWW WWWW WWW",
     "W                            W",
     "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"],

    # LEVEL 3
    ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
     "W                            W",
     "W WWW WWWWW WWW WW WWWWW WWW W",
     "W WSW WSSSW WSW WW WWWWW WSW W",
     "W WWW WWWWW WWW WW       WWW W",
     "W               WW WWWWWWWWWWW",
     "WWWWWWWWWWW W WW W WSSSSSSSSSS",
     "SSSSSSSSSSW W WW W WSSSSSSSSSS",
     "SSSSSSSSSSW W WW W WSSSSSSSSSS",
     "SSSSSSSSSSW W WW W WSSSSSSSSSS",
     "SSSSSSSSSSW W WW W WSSSSSSSSSS",
     "SSSSSSSSSSW W E  W WSSSSSSSSSS",
     "SSSSSSSSSSW W EE W WSSSSSSSSSS",
     "SSSSSSSSSSW WWWWWW WSSSSSSSSSS",
     "SSSSSSSSSSW WSSSSW WSSSSSSSSSS",
     "SSSSSSSSSSW WSSSSW WSSSSSSSSSS",
     "SSSSSSSSSSW WSSSSW WSSSSSSSSSS",
     "SSSSSSSSSSW WWWWWW WSSSSSSSSSS",
     "WWWWWWWWWWW WWWWWW WWWWWWWWWWW",
     "W                        W   W",
     "W WWWWWWWWWWW WWWWWWWWWW W W W",
     "W WWWWWWWWWWW WWWWWWWWWW W W W",
     "W                  W         W",
     "W WWWWWWWWWWWWWWWWWWWWWWWWWW W",
     "W W          WWWWWWWWWWWWWWW W",
     "W W WWWWWWWW W               W",
     "W   W      W W WWWWWWWWWWWWW W",
     "WWW   WWWW     W             W",
     "W   W      WWW   WWWWWWWWWWW W",
     "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",]
]
