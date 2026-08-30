# This is the purplePuncher class.
# The purplePuncher class extends the ghost class.
# The purplePuncher is stronger than the goldGhost as it has two attacks: softPunch and hardPunch.
# softPunch is a weaker attack that does less damage than hardPunch (but more than the goldGhost's attack).
# hardPunch is a stronger attack that does more damage than softPunch.

import ghost, random

PURPLE_PUNCHER_BASE_DAMAGE = 15

class purplePuncher(ghost):
    def __init__(self):
        super().__init__("Purple Puncher", 50, 2, 2)

    def softPunch(self, luigi):
        damage = PURPLE_PUNCHER_BASE_DAMAGE + self.skill * random.randint(1, 3)
        luigi.takeDamage(damage)
        print(f"{self.name} punches {luigi.name} for {damage} damage!")

    def hardPunch(self, luigi):
        damage = PURPLE_PUNCHER_BASE_DAMAGE + self.skill * random.randint(5, 10)
        luigi.takeDamage(damage)
        print(f"{self.name} lands a left hook onto {luigi.name} for {damage} damage! It's extra painful!")