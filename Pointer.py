import pygame 
import Constants
class Pointer:
    def __init__(self, color):
        self.color = color
        self.image = pygame.Surface((Constants.pix_sz * 0.25, Constants.pix_sz * 0.25)).convert()
        self.rect = self.image.get_rect()

    def update(self, new_x, new_y):
        # Updates position
        self.rect.centerx = new_x
        self.rect.centery = new_y