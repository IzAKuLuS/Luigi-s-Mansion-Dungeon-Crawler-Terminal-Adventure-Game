"""
This is the smallHeart class.
This class extends the item class.
This class represents a small heart item that gives luigi health
"""

SMALL_HEART_HEALTH = 25

from item import item


class smallHeart(item):
    def __init__(self):
        super().__init__("Small Heart", "This is a small heart. It heals 25 health.", "smallHeart", SMALL_HEART_HEALTH)