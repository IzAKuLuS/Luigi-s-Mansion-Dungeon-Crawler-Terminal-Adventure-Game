
"""
This is the largeArmor class.
The largeArmor class extends the item class.
The largeArmor class represents a large armor item that allows luigi to shield attacks up to 5 hits.
Armor works by halving the damage magnitude that an enemy inflicts onto the player.
"""
from item import item

LARGE_ARMOR_SLOTS = 3
LARGE_ARMOR_DURABILITY = 5

class largeArmor(item):
    def __init__(self):
        super().__init__(

            LARGE_ARMOR_SLOTS,
        )
        self.durability = LARGE_ARMOR_DURABILITY
