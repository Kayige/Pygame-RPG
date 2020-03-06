import pygame 
import Constants

class BossEnemy:
    def __init__(self, enemy, position):
        self.image = pygame.image.load(Constants.BOSS)
        self.rect = self.image.get_rect()
        self.enemy = enemy
        self.name = "Omega"
        self.variant = "undead"
        self.position = position
        self.health = 200
        self.max_health = 200
        self.downed = False
        self.defense = 0
        self.attack = 45
        self.exp_drop = 1
        self.gil_drop = 1
        self.weaken_debonus = 0
        self.weaken_dura = 0
        self.rect.centerx = Constants.win_w * 0.15
        self.rect.y = Constants.win_h * (0.2 * self.position)
 
