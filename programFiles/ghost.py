

import character

class ghost(character):
    def __init__(self, name, health, skill, numAttacks):
        super().__init__(name, health, skill)
        self.numAttacks = numAttacks
