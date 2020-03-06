class Equipment:
    def __init__(self, name, variant, attack, defense, value, can_equip):
        self.name = name
        self.variant = variant
        self.attack = attack
        self.defense = defense
        self.targets = (4, 5, 6, 7)
        self.buy_value = value
        self.sell_value = value * 0.5
        self.can_equip = can_equip