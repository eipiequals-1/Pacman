import pygame

class Button:
    def __init__(self, color, x, y, w, h, text=""):
        self.color = color
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.over_color = self.get_new_color()

    def draw(self, surface, pos, size=35, outline=None, font="uroob", font_color=(255, 255, 255)):
        border = 4
        if outline:
            pygame.draw.rect(surface, outline, (self.rect.x - border, self.rect.y - border, self.rect.width + border*2, self.rect.height + border*2))

        if not self.is_over(pos):
            pygame.draw.rect(surface, self.color, self.rect)
        else:
            pygame.draw.rect(surface, self.over_color, self.rect)
            
        if self.text != '':
            font = pygame.font.SysFont(font, size)
            writing = font.render(self.text, 1, font_color)
            surface.blit(writing, (self.rect.centerx - writing.get_width()//2, self.rect.centery - writing.get_height()//2))

    def is_over(self, pos):
        if pos[0] > self.rect.x and pos[0] < self.rect.x + self.rect.width:
            if pos[1] > self.rect.y and pos[1] < self.rect.y + self.rect.height:
                return True
        else:
            return False


    def get_new_color(self):
        r = self.color[0]
        g = self.color[1]
        b = self.color[2]

        new_r = r + 30
        new_g = g + 30
        new_b = b + 30
        if new_r > 255:
            new_r = r - 30
        if new_g > 255:
            new_g = g - 30
        if new_b > 255:
            new_b = b - 30

        return (new_r, new_g, new_b)
