import pygame 
import Constants

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, name, location):
        pygame.sprite.Sprite.__init__(self)
        self.x = x * Constants.pix_sz
        self.y = y * Constants.pix_sz
        self.variant = "block"
        self.color = Constants.BLACK

        # Platforms for town
        if location == "town":
            # Grass
            if name == " ":
                self.color = Constants.LIGHT_GREEN
            # Tree
            elif name == "T":
                self.color = Constants.GREEN
            # Dirt
            elif name == "D":
                self.color = Constants.LIGHT_BROWN
            # Path
            elif name == "P":
                self.color = Constants.BROWN
            # Wall
            elif name == "W":
                self.color = Constants.GRAY
                self.variant = "wall"
        # Platforms for world
        elif location == "world":
            # Ocean
            if name == " ":
                self.color = Constants.LIGHT_BLUE
                self.variant = "wall"
            # Grass
            elif name == "G":
                self.color = Constants.LIGHT_GREEN
                self.variant = "grass"
            # Forest
            elif name == "F":
                self.color = Constants.GREEN
                self.variant = "forest"
            # Rock
            elif name == "R":
                self.color = Constants.BROWN
                self.variant = "wall"
            # Dirt
            elif name == "D":
                self.color = Constants.LIGHT_BROWN
                self.variant = "dirt"
            # Path
            elif name == "P":
                self.color = Constants.BROWN
                self.variant = "path"
        # Platforms for castle
        elif location == "castle":
            # Floor
            if name == " ":
                self.color = Constants.LIGHT_GRAY
                self.variant = "floor"
            # Wall
            elif name == "W":
                self.color = Constants.GRAY
                self.variant = "wall"
   
        self.image = pygame.Surface((Constants.pix_sz, Constants.pix_sz))
        self.image.convert()
        self.image.fill(self.color)
        self.rect = pygame.Rect(x, y, Constants.pix_sz, Constants.pix_sz)