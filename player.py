import pygame, random
from pygame.locals import *
from constants import ROWS, COLS, CELL_W, CELL_H, VEC, FPS, WIDTH, HEIGHT, BOTTOM_BUFFER, PLAYER_START_POS


class Player:

    SIZE = CELL_W*2 // 3
    R_IMGS = [pygame.transform.scale(pygame.image.load("assets/player_open.png"), (SIZE, SIZE)), pygame.transform.scale(pygame.image.load("assets/player_closing.png"), (SIZE, SIZE)), pygame.transform.scale(pygame.image.load("assets/player_closed.png"), (SIZE, SIZE))]
    L_IMGS = [pygame.transform.flip(R_IMGS[0], True, False), pygame.transform.flip(R_IMGS[1], True, False), pygame.transform.flip(R_IMGS[2], True, False),]
    U_IMGS = [pygame.transform.rotate(R_IMGS[0], 90), pygame.transform.rotate(R_IMGS[1], 90), pygame.transform.rotate(R_IMGS[2], 90)]
    D_IMGS = [pygame.transform.rotate(R_IMGS[0], 270), pygame.transform.rotate(R_IMGS[1], 270), pygame.transform.rotate(R_IMGS[2], 270)]

    def __init__(self, level_num):
        self.grid_pos = PLAYER_START_POS
        self.pix_pos = VEC(self.grid_pos.x*CELL_W + (CELL_W//2), self.grid_pos.y*CELL_H + (CELL_H//2))
        self.direction = VEC(1, 0)
        self.new_dir = self.direction
        self.can_move = True
        self.sprite_count = 0
        self.lives = level_num + 1
        self.vel = 2
        self.old_pos = self.grid_pos
        
    def draw(self, surface):
        if self.sprite_count + 1 >= FPS:
            self.sprite_count = 0
        
        if self.direction == VEC(1, 0):
            surface.blit(self.R_IMGS[self.sprite_count//(FPS//3)], (self.pix_pos.x - self.SIZE//2, self.pix_pos.y - self.SIZE//2))
            self.sprite_count += 1

        if self.direction == VEC(-1, 0):
            surface.blit(self.L_IMGS[self.sprite_count//(FPS//3)], (self.pix_pos.x - self.SIZE//2, self.pix_pos.y - self.SIZE//2))
            self.sprite_count += 1

        if self.direction == VEC(0, 1):
            surface.blit(self.D_IMGS[self.sprite_count//(FPS//3)], (self.pix_pos.x - self.SIZE//2, self.pix_pos.y - self.SIZE//2))
            self.sprite_count += 1

        if self.direction == VEC(0, -1):
            surface.blit(self.U_IMGS[self.sprite_count//(FPS//3)], (self.pix_pos.x - self.SIZE//2, self.pix_pos.y - self.SIZE//2))
            self.sprite_count += 1

            
    def update(self, surface, maze):
        self.draw(surface)
        self.update_grid_pos()
        
        if self.can_move:
            self.pix_pos += self.direction*self.vel
        
        if self.time_to_turn():
            self.direction = self.new_dir
            self.can_move = self.check_wall(maze)

    def update_grid_pos(self):
        self.grid_pos.x = self.pix_pos.x//COLS
        self.grid_pos.y = self.pix_pos.y//ROWS


    def check_wall(self, maze):
        for wall in maze.walls:
            if VEC(self.grid_pos + self.direction) == wall:
                return False
        return True
        
    def time_to_turn(self):
        if (int(self.pix_pos.x - (CELL_W//2))) % CELL_W == 0 and (int(self.pix_pos.y - (CELL_H//2))) % CELL_H == 0:
            if self.new_dir == VEC(-1, 0) or self.new_dir == VEC(1, 0) or self.new_dir == VEC(0, 0) or self.new_dir == VEC(0, 1) or self.new_dir == VEC(0, -1) or self.new_dir == VEC(0, 0):
                return True

    def on_coin(self, coin):
        if self.grid_pos == coin:
            return True
        else:
            return False


    def draw_lives(self, surface):
        for i in range(self.lives):
            surface.blit(self.R_IMGS[1], (WIDTH*2//3 + (i*35 + self.SIZE), HEIGHT - self.SIZE//2 - BOTTOM_BUFFER//2))

            
    def reset(self, maze):
        self.grid_pos = self.set_player_start_pos(maze)
        self.pix_pos = VEC(self.grid_pos.x*CELL_W + (CELL_W//2), self.grid_pos.y*CELL_H + (CELL_H//2))
        self.new_dir = self.direction
        self.can_move = True
        self.sprite_count = 0
        self.vel = 2

    def set_player_start_pos(self, maze):
        num = 1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("crashed in the player pos generator", num)
                    pygame.quit()

            temp_pos = VEC(random.randint(0, COLS-1), random.randint(0, ROWS-1))
            if temp_pos in maze.coins and temp_pos != self.grid_pos:
                for dis in self.get_dis_to_enemy(maze, temp_pos):
                    if dis >= 8:
                        if temp_pos + VEC(1, 0) not in maze.walls:
                            self.direction = VEC(1, 0)
                        elif temp_pos + VEC(-1, 0) not in maze.walls:
                            self.direction = VEC(-1, 0)
                        elif temp_pos + VEC(0, 1) not in maze.walls:
                            self.direction = VEC(0, 1)
                        else:
                            self.direction = VEC(0, -1)
                        break
                break
            num += 1

        return temp_pos

    def get_dis_to_enemy(self, maze, player_pos):
        dis_to_enemies = []
        for enemy in maze.enemies:
            dis_to_enemies.append(abs(enemy.grid_pos.x - player_pos.x) + abs(enemy.grid_pos.y - player_pos.y))

        return dis_to_enemies


    def check_if_new_pos(self):
        if self.grid_pos != self.old_pos:
            self.old_pos = self.grid_pos
            return True
        else:
            return False
