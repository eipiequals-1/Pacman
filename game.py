import pygame, sys
from pygame.locals import *
from constants import *
from player import Player
from maze import Maze
from gui_parts.button import Button
from high_score import HighScore

class Game:
    """Handles game states such as menu, playing, and game over
    Handles events such as button presses and drawing windows
    
    """
    
    def __init__(self):
        self.SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption("Pacman")
        pygame.init()
        self.running = True
        self.state = "menu"
        self.level = 1

    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing(self.SCREEN)
            elif self.state == "menu":
                self.menu(self.SCREEN)
            elif self.state == "win":
                self.win(self.SCREEN)
            elif self.state == "lose":
                self.lose(self.SCREEN)
            elif self.state == "select":
                self.select(self.SCREEN)

        pygame.quit()
        sys.exit()
        
    def playing(self, surface):
        # Handles the maze, player, and enemy
        run = True
        maze = Maze(self.level)
        global SCORE
        SCORE = 0 # reset the score each time the player begins again
        while run:
            for event in pygame.event.get(): # checks events
                if event.type == pygame.QUIT:
                    HighScore.write(SCORE)
                    run = False
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        maze.player.new_dir = VEC(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        maze.player.new_dir = VEC(1, 0)
                    elif event.key == pygame.K_DOWN:
                        maze.player.new_dir = VEC(0, 1)
                    elif event.key == pygame.K_UP:
                        maze.player.new_dir = VEC(0, -1)

            # checks win or lose conditions
            if maze.get_win():
                HighScore.write(SCORE)
                run = False
                self.state = "win"

            if maze.get_lose():
                HighScore.write(SCORE)
                run = False
                self.state = "lose"

            if maze.player_on_coin():
                SCORE += 10

            # redraws the windo every frame
            surface.fill(BLACK)
            maze.update(surface)
            self.display_text(surface, 200, HEIGHT - 40, "SCORE: " + str(SCORE))
            maze.player.draw_lives(surface)
            pygame.display.update()
            self.CLOCK.tick(FPS)

    def menu(self, surface):
        run = True
        start = Button(BLUE, WIDTH//2 - 55, HEIGHT*13//25, 110, 40, "GO!")
        select_level = Button(ORANGE, WIDTH//2 - 80, HEIGHT*15//25, 160, 60, "LEVEL SELECT")
        while run:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start.is_over(pos):
                        run = False
                        self.state = "playing"
                    if select_level.is_over(pos):
                        run = False
                        self.state = "select"
                    
            surface.fill(BLACK)
            self.display_text(surface, WIDTH//2, HEIGHT*10//25, "PACMAN", 90, "uroob", False, ORANGE, True)
            self.display_text(surface, WIDTH//2, HEIGHT*1//50, "HIGH SCORE: " + str(HighScore.get_max()), 30, "uroob", False, ORANGE, True)
            self.display_text(surface, WIDTH//2, HEIGHT*48//50, "1 PLAYER ONLY", 30, "uroob", False, TURQUOISE, True)
            #karumbi, nakula, tlwgtypist, uroob
            start.draw(surface, pos)
            select_level.draw(surface, pos)
            pygame.display.update()
            self.CLOCK.tick(FPS)

    def lose(self, surface):
        run = True
        again = Button(ORANGE, WIDTH//5, HEIGHT - 70, 130, 60, "TRY AGAIN")
        home = Button(BLUE, WIDTH*4//5 - 130, HEIGHT - 70, 130, 60, "MENU")
        while run:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if again.is_over(pos):
                        run = False
                        self.state = "playing"
                    if home.is_over(pos):
                        run = False
                        self.state = "menu"

            surface.fill(BLACK)
            self.display_text(surface, WIDTH//2, HEIGHT//2, "The Ghosts caught you", 40, "uroob", False, YELLOW, True)
            self.display_text(surface, WIDTH//2, HEIGHT*14//25, "SCORE: " + str(SCORE), 30, "uroob", True, ORANGE, True, True)
            again.draw(surface, pos)
            home.draw(surface, pos)
            pygame.display.update()
            self.CLOCK.tick(FPS)

    def win(self, surface):
        run = True
        next_level = Button(GREY, WIDTH//5, HEIGHT - 70, 130, 60, "CONTINUE")
        home = Button(BLUE, WIDTH*4//5 - 130, HEIGHT - 70, 130, 60, "MENU")
        while run:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_level.is_over(pos):
                        run = False
                        if self.level < 3:
                            self.level += 1
                            self.state = "playing"
                        else:
                            self.level = 1
                            self.state = "menu"
                    if home.is_over(pos):
                        run = False
                        self.state = "menu"

            self.display_text(surface, WIDTH//2, HEIGHT//2, "Great Escape!", 40, "rachana", True, YELLOW, True)
            self.display_text(surface, WIDTH//2, HEIGHT*15//25, "S C O R E : " + str(SCORE), 40, "uroob", False, YELLOW, True)
            next_level.draw(surface, pos)
            home.draw(surface, pos)
            pygame.display.update()
            self.CLOCK.tick(FPS)

    def select(self, surface):
        img_size = 350
        button_height = 60
        top = (HEIGHT - (img_size*2) - (button_height*2))//3
        L1_IMG = pygame.transform.scale(pygame.image.load("assets/level_1.png").convert_alpha(), (img_size, img_size))
        l1 = Button(PURPLE, top, top + img_size, img_size, button_height, "LEVEL 1")
        L2_IMG = pygame.transform.scale(pygame.image.load("assets/level_2.png").convert_alpha(), (img_size, img_size))
        l2 = Button(PURPLE, WIDTH - img_size - top, top + img_size, img_size, button_height, "LEVEL 2")
        L3_IMG = pygame.transform.scale(pygame.image.load("assets/level_3.png").convert_alpha(), (img_size, img_size))
        l3 = Button(PURPLE, WIDTH//2 - img_size//2, HEIGHT - top*2, img_size, button_height, "LEVEL 3")
        home = Button(TURQUOISE, WIDTH - 100, HEIGHT - 60, 90, 50, "BACK")
        
        run = True
        while run:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if l1.is_over(pos):
                        run = False
                        self.level = 1
                        self.state = "playing"
                    if l2.is_over(pos):
                        run = False
                        self.level = 2
                        self.state = "playing"
                    if l3.is_over(pos):
                        run = False
                        self.level = 3
                        self.state = "playing"
                    if home.is_over(pos):
                        run = False
                        self.state = "menu"
                    
            surface.fill(BLACK)
            surface.blit(L1_IMG, (top, top))
            surface.blit(L2_IMG, (WIDTH - img_size - top, top))
            surface.blit(L3_IMG, (WIDTH//2 - img_size//2, HEIGHT - top*2 - img_size))
            l1.draw(surface, pos, 55, TURQUOISE)
            l2.draw(surface, pos, 55, TURQUOISE)
            l3.draw(surface, pos, 55, TURQUOISE)
            home.draw(surface, pos)
            pygame.display.update()
            self.CLOCK.tick(FPS)
            
    @staticmethod
    def draw_grid(surface, rows, cols):
        for i in range(rows + 1):
            pygame.draw.line(surface, WHITE, (0, i * CELL_H), (WIDTH, i * CELL_H))
        for i in range(cols + 1):
            pygame.draw.line(surface, WHITE, (i * CELL_W, 0), (i * CELL_H, HEIGHT - BOTTOM_BUFFER))

    @staticmethod
    def display_text(surface, x, y, text='Choose a text!', size=35, font_name="uroob", bold=True, color=(200, 200, 200), centered=False, italics=False):
        font = pygame.font.SysFont(font_name, size, bold, italics)
        writing = font.render(text, 1, color)
        if centered:
            surface.blit(writing, (WIDTH//2 - writing.get_width()//2, y))
        else:
            surface.blit(writing, (x, y))
