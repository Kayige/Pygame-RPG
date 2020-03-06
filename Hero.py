import random 

class Hero:
    def __init__(self, equip_list, run):
        self.run = run
        self.equip_list = equip_list

    def check_health(self, c, hero_list):
        # Checks health to see if it is within bounds
        # If <= 0 health, character is downed
        if c.health <= 0:
            c.health = 0
            c.downed = True
            print(c.name + " is downed")
        else:
            c.downed = False

        # If health exceeds max, current health = max health
        if c.health > c.max_health:
            c.health = c.max_health

        # If energy exceeds max, current energy = max energy
        if c.energy > c.max_energy:
            c.energy = c.max_energy

        print(c.name + ": Health: " + str(c.health) + " / " + str(c.max_health))
        print(c.name + ": Energy: " + str(c.energy) + " / " + str(c.max_energy))
        print(" ")

        new_text_list = []
        for line in range(0, 4):
            if len(hero_list) - 1 >= line:
                new_text_list += [hero_list[line].name + ": " + "HP: " + str(hero_list[line].health) + " / "
                                  + str(hero_list[line].max_health)]
                new_text_list += ["       EP: " + str(hero_list[line].energy) + " / " + str(hero_list[line].max_energy)]
            else:
                new_text_list += [""]

        self.run.textbox_health.update(new_text_list)
    
    def check_buffs(self, character):
        # Checks to see if buffs should be active, if not, then deactivates them
        # Checks for Temper
        if character.temper_dura >= 1:
            if character.temper_dura == 1:
                print("Temper has worn off")
                character.temper_bonus = 0
            character.temper_dura -= 1

        # Checks for Defend
        if character.defend_dura >= 1:
            if character.defend_dura == 1:
                print("Defend has worn off")
                character.defend_bonus = 0
            character.defend_dura -= 1

        # Checks for Protect
        if character.protect_dura >= 1:
            if character.protect_dura == 1:
                print("Protect has worn off")
                character.protect_bonus = 0
            character.protect_dura -= 1
    
    def attack(self, player, source, hero_list, enemy_list):
        # Character performs action based on previously determined inputs
        print("Turn: " + source.name)
        if not source.downed:
            action = source.g_name[1][source.pos_list[0]][0]
            self.run.textbox_prompt.message([source.name + ": " + action, "", "", "", "", "", "", ""])
            # Attack
            if source.pos_list[0] == 0:
                target = enemy_list[source.pos_list[1]]
                print("Attacking " + str(target.name) + " " + str(target.position))
                self.damage(source.attack * (1 + source.temper_bonus), target, enemy_list)
            # Defending has no action, but instead a buff applied before all other actions are taken
            elif source.pos_list[0] == 1:
                print("Defending")
            # Spells
            elif source.pos_list[0] == 2:
                magic = source.spell_list[source.pos_list[1]]
                print("Casting " + magic.name)
                # Determines effect of spell depending on variant
                # If variant is attack/heal, effect is the damage/healing done
                if magic.variant == "attack":
                    target = enemy_list[source.pos_list[2]]
                    self.damage(magic.effect * (1 + source.temper_bonus), target, enemy_list)
                elif magic.variant == "heal":
                    target = hero_list[source.pos_list[2]]
                    self.damage(magic.effect * (1 + source.temper_bonus), target, hero_list)
                # If variant is attack_all/heal_all, effect is the damage/healing done to all members
                elif magic.variant == "attack_all":
                    for target in enemy_list:
                        if not target.downed:
                            # If magic casted is Dia, target must also be undead to take damage
                            if (magic.name == "Dia" and target.variant == "undead") or magic.name != "Dia":
                                self.damage(magic.effect * (1 + source.temper_bonus), target, enemy_list)
                elif magic.variant == "heal_all":
                    for target in hero_list:
                        if not target.downed:
                            self.damage(magic.effect * (1 + source.temper_bonus), target, hero_list)
                # If variant is buff/debuff, effect is constant that multiplies with other values
                elif magic.variant == "buff":
                    target = hero_list[source.pos_list[2]]
                    if magic.name == "Protect":
                        target.protect_bonus = magic.effect
                        target.protect_dura = 3
                    elif magic.name == "Temper":
                        target.temper_bonus = magic.effect
                        target.temper_dura = 3
                elif magic.variant == "debuff":
                    target = enemy_list[source.pos_list[2]]
                    if magic.name == "Weaken":
                        target.weaken_debuff_bonus = magic.effect
                        target.weaken_dura = 3

                # Subtracts energy cost of spell from character
                print("Cost: " + str(magic.cost))
                source.energy -= magic.cost
                self.check_health(source, hero_list)
            # Items
            elif source.pos_list[0] == 3:
                item = source.g_obj[1][3][1][source.pos_list[1]][0]
                target = hero_list[source.pos_list[2]]
                print("Using " + item.name + " on " + target.name)
                item.use_item(target)
                target.hero.check_health(target, hero_list)
            # Run
            elif source.pos_list[0] == 4:
                # Gives a chance for the party to run away
                print(source.name + " is attempting to run away.")
                chance = random.random() * 100
                print(chance)
                if chance > 40:
                    print("The party ran away successfully.")
                    print(" ")
                    return "run success"
                else:
                    print("The party did not manage to run away.")
                    print(" ")
                    return "run fail"
        else:
            self.run.textbox_prompt.message([source.name + " is downed.", "", "", "", "", "", "", ""])
            print(source.name + " is downed.")
        print(" ")
        return "None"

    def damage(self, attack, target, target_list):
        # Deals damage / heals to target
        # If attack is positive, damage is dealt to enemy based on base damage times the damage negation (defense)
        if attack >= 0:
            dam = random.randrange(int(attack * 0.7), int(attack * 1.3))
            # If selected enemy is downed, attacks another random enemy
            if target.downed:
                targets = []
                for e in target_list:
                    if not e.downed:
                        targets += [e]
                target = random.sample(targets, 1)[0]

            dam_negate = (100 - target.defense) / 100
            print("dam_negate: " + str(dam_negate))
            dam_dealt = int(dam * dam_negate)
            target.health -= dam_dealt
            print(target.name + " takes " + str(dam_dealt) + " damage.")
            target.enemy.check_health(target)
        # If attack is negative, target is healed for amount of damage given
        else:
            heal_dealt = random.randrange(int(attack * 1.3), int(attack * 0.7))
            if not target.downed:
                target.health -= heal_dealt
                print(target.name + " is healed for " + str(- heal_dealt) + " health.")
                target.hero.check_health(target, target_list)
            else:
                print("Spell has no effect, target is downed.")

    def update_stats(self, target):
        # Updates character's stats to reflect level and equipment
        target.max_health = int(target.max_health_base * target.multiplier)
        target.max_energy = int(target.max_energy_base * target.multiplier)
        target.attack = int((target.attack_base + target.weapon.attack + target.armor.attack) * target.multiplier)
        target.defense = int((target.defense_base + target.weapon.defense + target.armor.defense) * target.multiplier)