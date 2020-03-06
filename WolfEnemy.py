import pygame
import Constants

class WolfEnemy:
    def __init__(self, enemy, position):
        self.image = pygame.image.load("Wolf.png")
        self.rect = self.image.get_rect()
        self.enemy = enemy
        self.name = "Wolf"
        self.variant = "living"
        self.position = position
        self.health = 15
        self.max_health = 15
        self.downed = False
        self.defense = 0
        self.attack = 17
        self.exp_drop = 17
        self.gil_drop = 15
        self.weaken_debonus = 0
        self.weaken_dura = 0
        self.rect.centerx = Constants.win_w * 0.15
        self.rect.y = Constants.win_h * (0.2 * self.position)
       
