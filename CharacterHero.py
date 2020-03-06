import pygame
import Constants

class CharacterHero:
    def __init__(self, name, variant, position, class_list, spell_list, run, hero, image_fill):
        # Appearance on screen
        self.name = name
        self.image = pygame.image.load(image_fill)
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.centerx = Constants.win_w * 0.85
        self.rect.y = Constants.win_h * (0.00 + 0.15 * self.position)
        self.run = run
        self.hero = hero

        # Class stats
        self.variant = variant
        self.health = class_list[self.variant][0]
        self.max_health = class_list[self.variant][0]
        self.max_health_base = class_list[self.variant][0]
        self.energy = class_list[self.variant][1]
        self.max_energy = class_list[self.variant][1]
        self.max_energy_base = class_list[self.variant][1]
        self.attack = class_list[self.variant][2]
        self.attack_base = class_list[self.variant][2]
        self.defense = class_list[self.variant][3]
        self.defense_base = class_list[self.variant][3]
        self.use_magic = class_list[self.variant][4]

        # Determines usable magic based on class's ability to use magic
        if self.use_magic == 1:
            self.spell_list = [spell_list[0], spell_list[1], spell_list[2]]
        elif self.use_magic == 2:
            self.spell_list = [spell_list[4], spell_list[5], spell_list[6]]
        elif self.use_magic == 3:
            self.spell_list = [spell_list[0], spell_list[1], spell_list[6]]
        else:
            self.spell_list = ["None", "None", "None"]

        # Settings
        self.weapon = self.hero.equip_list[-2]
        self.armor = self.hero.equip_list[-1]
        self.level = 1
        self.multiplier = 1
        self.exp = 0
        self.exp_needed = 50
        self.downed = False
        self.temper_bonus = 0
        self.temper_dura = 0
        self.defend_bonus = 0
        self.defend_dura = 0
        self.protect_bonus = 0
        self.protect_dura = 0

        # Menu settings for combat
        self.pos_list = 0
        self.g_obj = 0
        self.g_name = 0
 
    def update_class(self, class_list, variant):
        # Updates class of default characters at character creation
        self.variant = variant
        self.health = class_list[self.variant][0]
        self.max_health = class_list[self.variant][0]
        self.max_health_base = class_list[self.variant][0]
        self.energy = class_list[self.variant][1]
        self.max_energy = class_list[self.variant][1]
        self.max_energy_base = class_list[self.variant][1]
        self.attack = class_list[self.variant][2]
        self.attack_base = class_list[self.variant][2]
        self.defense = class_list[self.variant][3]
        self.defense_base = class_list[self.variant][3]
        self.use_magic = class_list[self.variant][4]
 
    def update_selection(self, select_list):
        # Stores selection from character's turn to be used during their action
        self.pos_list = select_list[0]
        self.g_obj = select_list[1]
        self.g_name = select_list[2]
 
    def shift(self, x_offset, hero_list, enemy_list):
        # Moves Character's rect over by x_offset over time, blits all in combat_loop
        self.rect.x += x_offset

        # Renders game
        self.run.screen.fill(Constants.WHITE)

        for textbox in self.run.textbox_combat_list:
            textbox.textbox_blit()

        for c in hero_list:
            self.run.screen.blit(c.image, c.rect)

        for e in enemy_list:
            if not e.downed:
                 self.run.screen.blit(e.image, e.rect)

        # Writes to main surface
        pygame.display.flip()
