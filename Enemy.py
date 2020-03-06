import pygame 
import random 
import Constants

class Enemy:
    def __init__(self, run):
          self.run = run

    def check_health(self, e):
        # Checks health to see if it is within bounds
        # If <= 0 health, character is downe
        if e.health <= 0:
            e.health = 0
            e.downed = True
            print(e.name + " " + str(e.position) + " is downed")
        else:
            e.downed = False
        # If health exceeds max, current health = max health
        if e.health > e.max_health:
            e.health = e.max_health

        print(e.name + " " + str(e.position) + ": " + str(e.health) + " / " + str(e.max_health))

    def attack(self, source, hero_list):
        # Enemy Selects a random (not downed) hero to attack
        if not source.downed:
            self.run.textbox_prompt.message([source.name + ": Attack", "", "", "", "", "", "", ""])
            print("Turn: " + source.name + " " + str(source.position))
            targets = []

            for c in hero_list:
                if not c.downed:
                    targets += [c]

            target = random.sample(targets, 1)[0]
            print("Attacking " + str(target.name))
            self.damage(random.randrange(int(source.attack * 0.7), int(source.attack * 1.3)), target, hero_list)
        else:
            print(source.name + " " + str(source.position) + " is downed")
        print(" ")

    def damage(self, dam, target, target_list):
        # Deals damage to target
        dam_negate = (100 - target.defense - target.protect_bonus) * (100 - target.defend_bonus) * 0.0001
        print("dam_negate: " + str(dam_negate))
        # Damage is dealt to enemy based on base damage times the damage negation (defense)
        if dam >= 0:
            dam_dealt = int(dam * dam_negate)
            target.health -= dam_dealt
            print(target.name + " takes " + str(dam_dealt) + " damage.")
            target.hero.check_health(target, target_list)

    def shift(self, x_offset, hero_list, enemy_list, target):
        # Moves Character's rect over by x_offset over time, blits all in combat_loop
        target.rect.x += x_offset
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
