class SpellVariant:
    def __init__(self, spell, name, variant, usable, targets, cost, effect_strength, out_of_combat, desc):
        # Defines a spell and its individual properties/effects
        self.spell = spell
        self.name = name
        self.variant = variant
        self.usable = usable
        self.targets = targets
        self.cost = cost

        # If variant is attack/heal, effect is the damage/healing done
        # If variant is attack_all/heal_all, effect is the damage/healing done to all members
        # If variant is buff/debuff, effect is constant that multiplies with other values
        self.effect = effect_strength

        # If true, spell can be used in pause menu (healing spells)
        self.out_of_combat = out_of_combat

        self.desc = desc