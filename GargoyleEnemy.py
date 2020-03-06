import pygame 
import Constants
import os

class GargoyleEnemy:
    def __init__(self, enemy, position):
        self.image = pygame.image.load(Constants.GARGOYLE)
        self.rect = self.image.get_rect()
        self.enemy = enemy
        self.name = "Gargoyle"
        self.variant = "undead"
        self.position = position
        self.health = 80
        self.max_health = 80
        self.downed = False
        self.defense = 0
        self.attack = 15
        self.exp_drop = 62
        self.gil_drop = 62
        self.weaken_debonus = 0
        self.weaken_dura = 0
        self.rect.centerx = Constants.win_w * 0.15
        self.rect.y = Constants.win_h * (0.2 * self.position)
        
