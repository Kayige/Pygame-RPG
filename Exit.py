import pygame 
import Constants

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, destination, dest_x, dest_y, location):
        pygame.sprite.Sprite.__init__(self)
        self.x = x * Constants.pix_sz
        self.y = y * Constants.pix_sz
        self.location = location
        self.destination = destination
        self.dest_x = dest_x * Constants.pix_sz
        self.dest_y = dest_y * Constants.pix_sz

        # Color
        if self.location == "town":
            self.color = Constants.GREEN
        elif self.location == "world":
            self.color = Constants.GRAY
        elif self.location == "castle":
            self.color = Constants.GRAY

        self.image = pygame.Surface((Constants.pix_sz, Constants.pix_sz))
        self.image.convert()
        self.image.fill(self.color)
        self.rect = pygame.Rect(self.x, self.y, Constants.pix_sz, Constants.pix_sz)