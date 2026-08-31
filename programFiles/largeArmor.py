import item

LARGE_ARMOR_SLOTS = 3

class largeArmor(item):
    def __init__(self):
        super().__init__("Large Armor", "Adds 3 armor slot.", "largeArmor", LARGE_ARMOR_SLOTS)
        