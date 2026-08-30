
# This is a largeHeart class extends the item class. 
# It represents a large heart item that can be used to heal Luigi in game.

LARGE_HEART_HEALTH = 100

import item

class largeHeart(item):
    def __init__(self):
        super().__init__("Large Heart", "This is a large heart. It heals 100 health.", "largeHeart");
        self.healingAmount = LARGE_HEART_HEALTH