class Item:
    def __init__(self, name, variant, strength, value, desc):
        self.name = name
        self.variant = variant
        self.strength = strength
        self.targets = (4, 5, 6, 7)
        self.buy_value = value
        self.sell_value = value * 0.5  
        self.desc = desc    

    def use_item(self, target):
        # Adds health
        if self.variant == "health":
            if target.downed:
                print("Item has no effect, target is downed")
            else:
                target.health += self.strength
        # Adds health (Phoenix down, revives downed party members)
        elif self.variant == "greater_health":
            target.health += self.strength
        # Adds energy
        elif self.variant == "energy":
            if target.downed:
                print("Item has no effect, target is downed")
            else:
                target.energy += self.strength