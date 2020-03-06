import pygame 
import Constants

class NoneEnemy:
    def __init__(self, enemy, position):
        self.image = pygame.Surface((32, 32)).convert()
        self.rect = self.image.get_rect()
        self.enemy = enemy
        self.name = "None-enemy"
        self.variant = "living"
        self.position = position
        self.health = 0
        self.max_health = 0
        self.downed = True
        self.defense = 0
        self.attack = 0
        self.exp_drop = 0
        self.gil_drop = 0
        self.weaken_debonus = 0
        self.weaken_dura = 0
        self.rect.centerx = Constants.win_w * 0.15
        self.rect.y = Constants.win_h * (0.2 * self.position)
        self.color = Constants.BLACK