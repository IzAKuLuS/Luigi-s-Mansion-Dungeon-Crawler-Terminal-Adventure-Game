import ghost, random

GOLD_GHOST_BASE_DAMAGE = 10

class goldGhost(ghost):
    def __init__(self):
        super().__init__("Gold Ghost", 30, 1, 1)

    def punch(self, luigi):
        damage = GOLD_GHOST_BASE_DAMAGE
        luigi.takeDamage(damage)
        print(f"{self.name} punches {luigi.name} for {damage} damage!")
