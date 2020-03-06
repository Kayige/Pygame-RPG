class Spell:
    def __init__(self, run):
        # Superclass to allow a spell to be used
        self.run = run  

    def use_spell(self, target, spell, source):
        # Casts spell, effect is based on type of spell and target
        source.energy -= spell.cost
        # Attacks/heals one target
        if spell.variant == "attack":
            target.health -= spell.effect
        # Attacks/heals all in spell's target list
        elif spell.variant == "attack_all":
            for t in spell.targets:
                t.health -= spell.effect
        # Debuffs target
        elif spell.variant == "status":
            if spell.name == "Weaken":
                target.weaken_debuff = spell.effect
        # Duration of Weaken is 3 Turns
                target.weaken_dura = 3
        # Buffs ally target
        elif spell.variant == "buff":
            if spell.name == "Protect":
                target.defense_multiplier = spell.effect
            elif spell.name == "Temper":
                target.attack_multiplier = spell.effect