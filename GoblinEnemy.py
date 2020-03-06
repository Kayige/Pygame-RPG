import pygame 
import Constants

class GoblinEnemy:
    def __init__(self, enemy, position):
        self.image = pygame.image.load(Constants.GOBLIN)
        self.rect = self.image.get_rect()
        self.enemy = enemy
        self.name = "Goblin"
        self.variant = "living"
        self.position = position
        self.health = 25
        self.max_health = 25
        self.downed = False
        self.defense = 0
        self.attack = 15
        self.exp_drop = 15
        self.gil_drop = 8
        self.weaken_debonus = 0
        self.weaken_dura = 0
        self.rect.centerx = Constants.win_w * 0.15
        self.rect.y = Constants.win_h * (0.2 * self.position)
        
