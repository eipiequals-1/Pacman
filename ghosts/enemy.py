import pygame
from pygame.locals import*
from constants import CELL_W, CELL_H, VEC, ROWS, COLS

class Enemy:    
    def __init__(self, pos, vel):
        self.PADDING = 4
        self.GHOST_D = pygame.transform.scale(pygame.image.load("assets/ghost_down.png"), (CELL_W - self.PADDING, CELL_H - self.PADDING))
        self.GHOST_L = pygame.transform.scale(pygame.image.load("assets/ghost_left.png"), (CELL_W - self.PADDING, CELL_H - self.PADDING))
        self.GHOST_U = pygame.transform.scale(pygame.image.load("assets/ghost_up.png"), (CELL_W - self.PADDING, CELL_H - self.PADDING))
        self.GHOST_R = pygame.transform.scale(pygame.image.load("assets/ghost_right.png"), (CELL_W - self.PADDING, CELL_H - self.PADDING))
        
        self.grid_pos = VEC(pos)
        self.pix_pos = VEC(self.grid_pos.x*CELL_W + (CELL_W//2), self.grid_pos.y*CELL_H + (CELL_H//2))
        self.direction = VEC(1, 0)
        self.new_dir = self.direction
        self.vel = vel
        self.target = None

    def draw(self, surface):
        if self.direction == VEC(0, -1):
            surface.blit(self.GHOST_U, (int(self.pix_pos.x - self.GHOST_U.get_width()//2), int(self.pix_pos.y - self.GHOST_U.get_height()//2)))
            
        elif self.direction == VEC(0, 1):
            surface.blit(self.GHOST_D, (int(self.pix_pos.x - self.GHOST_D.get_width()//2), int(self.pix_pos.y - self.GHOST_D.get_height()//2)))
            
        elif self.direction == VEC(1, 0):
            surface.blit(self.GHOST_R, (int(self.pix_pos.x - self.GHOST_R.get_width()//2), int(self.pix_pos.y - self.GHOST_R.get_height()//2)))

        elif self.direction == VEC(-1, 0):
            surface.blit(self.GHOST_L, (int(self.pix_pos.x - self.GHOST_L.get_width()//2), int(self.pix_pos.y - self.GHOST_L.get_height()//2)))


    def update(self, surface, maze):
        self.draw(surface)
        self.target = maze.player.grid_pos
        
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.vel
            if self.time_to_turn():
                self.move(maze)
        
        self.update_grid_pos()


    def update_grid_pos(self):
        self.grid_pos.x = self.pix_pos.x//COLS
        self.grid_pos.y = self.pix_pos.y//ROWS


    def breadth_first_search(self, maze, start, target):
        grid = [[0 for x in range(COLS)] for x in range(ROWS)]
        for cell in maze.walls:
            if cell.x < COLS and cell.y < ROWS:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("crashed in the 1st part of breadth first search")
                    pygame.quit()
                    
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbors = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbor in neighbors:
                    if neighbor[0]+current[0] >= 0 and neighbor[0] + current[0] < len(grid[0]):
                        if neighbor[1]+current[1] >= 0 and neighbor[1] + current[1] < len(grid):
                            next_cell = [neighbor[0] + current[0], neighbor[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("crashed in the 2nd part of breadth first search")
                    print(type(self))
                    pygame.quit()
            
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest
    

    def time_to_turn(self):
        if (int(self.pix_pos.x - (CELL_W//2))) % CELL_W == 0 and (int(self.pix_pos.y - (CELL_H//2))) % CELL_H == 0:
            if self.new_dir == VEC(-1, 0) or self.new_dir == VEC(1, 0) or self.new_dir == VEC(0, 0) or self.new_dir == VEC(0, 1) or self.new_dir == VEC(0, -1) or self.new_dir == VEC(0, 0):
                return True

    def get_path_direction(self, maze, target):
        next_cell = self.find_next_cell_in_path(maze, target)
        x_dir = next_cell[0] - self.grid_pos.x
        y_dir = next_cell[1] - self.grid_pos.y
        return VEC(x_dir, y_dir)

    def find_next_cell_in_path(self, maze, target):
        path = self.breadth_first_search(maze, [int(self.grid_pos.x), int(self.grid_pos.y)], [int(target[0]), int(target[1])])
        return path[1]


    def move(self, maze):
        self.direction = self.get_path_direction(maze, self.target)
