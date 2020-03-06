import pygame 

class Text:
    def __init__(self, size, text, align, x, y, color):
        self.font = pygame.font.SysFont("Britannic Bold", int(size))
        self.text = text
        self.color = color
        self.image = self.font.render(self.text, 1, color)
        self.rect = self.image.get_rect()
        self.align = align

        if self.align == "left":
            self.rect.x = x
            self.rect.y = y
        elif self.align == "center":
            self.rect.centerx = x
            self.rect.y = y

    def update_text(self, new_text):
        # Updates text
        self.text = new_text
        self.image = self.font.render(self.text, 1, self.color)

    def update_color(self, new_color):
        self.color = new_color
        self.image = self.font.render(self.text, 1, self.color)