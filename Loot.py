import pygame 
import Constants

class Loot(pygame.sprite.Sprite):
    def __init__(self, x, y, location, treasure):
        pygame.sprite.Sprite.__init__(self)
        self.x = x * Constants.pix_sz
        self.y = y * Constants.pix_sz
        self.location = location
        self.treasure = treasure
        self.unopened = True

        # Color

        self.image = pygame.image.load(Constants.CHEST)
        self.rect = pygame.Rect(self.x, self.y, Constants.pix_sz, Constants.pix_sz)
