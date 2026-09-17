"""
This is the smallArmor class.
This class extends the item class.
This class represents a small armor item that gives luigi armor that has 3 uses.
Armor works by halving the damage magnitude that an enemy inflicts onto the player.
"""

from item import item

SMALL_ARMOR_SLOTS = 1
SMALL_ARMOR_DURABILITY = 3

class smallArmor(item):
    def __init__(self):
        super().__init__(
            "Small Armor",
            "Halves damage from the next 3 ghost attacks.",
            "smallArmor",
            SMALL_ARMOR_SLOTS,
        )
        self.durability = SMALL_ARMOR_DURABILITY 
