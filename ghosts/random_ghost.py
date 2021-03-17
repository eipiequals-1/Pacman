import pygame, random
from pygame.locals import *
from .enemy import Enemy
from constants import VEC, ROWS, COLS

class Random(Enemy):
    def __init__(self, maze, pos, vel):
        super().__init__(pos, vel)
        self.target = self.get_random_target(maze)
        self.curr_target = self.target
        

    def move(self, maze):
        self.direction = self.get_path_direction(maze, self.target)

    def update(self, surface, maze):
        self.draw(surface)
        self.target = self.curr_target
        
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.vel
            if self.time_to_turn():
                self.move(maze)
        else:
            self.curr_target = self.get_random_target(maze)   
        
        self.update_grid_pos()
            

    def get_random_target(self, maze):
        pos_found = False
        while not pos_found:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("crashed in the random ghost module")
                    pygame.quit()
            temp_pos = VEC(random.randint(0, COLS-1), random.randint(0, ROWS-1))
            if temp_pos in maze.coins and temp_pos != self.grid_pos:
                pos_found = True

        return VEC(temp_pos)
