import pygame
import Constants

class OgreEnemy:
    def __init__(self, enemy, position):
        self.image = pygame.image.load(Constants.OGRE)
        self.rect = self.image.get_rect()
        self.enemy = enemy
        self.name = "Ogre"
        self.variant = "living"
        self.position = position
        self.health = 75
        self.max_health = 75
        self.downed = False
        self.defense = 25
        self.attack = 30
        self.exp_drop = 112
        self.gil_drop = 112
        self.weaken_debonus = 0
        self.weaken_dura = 0
        self.rect.centerx = Constants.win_w * 0.15
        self.rect.y = Constants.win_h * (0.2 * self.position)
        
