import pygame
from constants import WIDTH, HEIGHT, ROWS, COLS, CELL_H, CELL_W, LEVELS, BLUE, VEC, YELLOW, SCORE, PLAYER_START_POS
from ghosts.speed_ghost import Speedy
from ghosts.random_ghost import Random
from ghosts.slow_ghost import Slow
from player import Player

class Maze:
    def __init__(self, level_num):
        self.level_num = level_num
        self.walls = []
        self.coins = []
        self.enemies = []
        self.load_maze()

    def load_maze(self):
        ghost_count = 0
        for y, line in enumerate(LEVELS[self.level_num - 1]):
            for x, char in enumerate(line):
                if char == 'W':
                    self.walls.append(VEC(x, y))
                elif char == ' ':
                    self.coins.append(VEC(x, y))
                elif char == 'E':
                    ghost_count += 1
                    if ghost_count == 1:
                        self.enemies.append(Speedy(VEC(x, y), 1.5))
                    elif ghost_count == 2:
                        self.enemies.append(Random(self, VEC(x, y), 2))
                    elif ghost_count == 3:
                        self.enemies.append(Slow(VEC(x, y), 1))
        self.player = Player(self.level_num)

                        
    def draw_maze(self, surface):
        for wall in self.walls:
            pygame.draw.rect(surface, BLUE, (wall.x*CELL_W, wall.y*CELL_H, CELL_W, CELL_H))

        for coin in self.coins:
            pygame.draw.circle(surface, YELLOW, (int(coin.x*CELL_W + (CELL_W//2)), int(coin.y * CELL_H + (CELL_H//2))), CELL_W//6)


    def update(self, surface):
        self.draw_maze(surface)

        for enemy in self.enemies:
            enemy.update(surface, self)
            if enemy.grid_pos == self.player.grid_pos:
                self.player.lives -= 1
                self.player.reset(self)
                
        self.player.update(surface, self)

    def get_win(self):
        if len(self.coins) == 0:
            return True

    def get_lose(self):
        if self.player.lives <= 0:
            return True
        else:
            return False

    def player_on_coin(self):
        for index, coin in enumerate(self.coins):
            if self.player.on_coin(coin):
                self.coins.pop(index)
                return True
