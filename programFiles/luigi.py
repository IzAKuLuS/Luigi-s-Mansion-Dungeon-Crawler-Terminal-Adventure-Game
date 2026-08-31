
# This is the luigi class.
# The luigi class extends the character class
# The luigi class adds an inventory to the character class that allows luigi to obtain/store items.
# The inventory is a dictionary that contains two dictionaries: one for hearts and one for armor.

import item, character, luigi_funcs

SMALL_HEART_HEALTH = 25
LARGE_HEART_HEALTH = 100

VACUUM_BASE_DAMAGE = 15

SMALL_ARMOR_VALUE = 1
LARGE_ARMOR_VALUE = 3

ITEM_ARRAY_SIZE = 3


# This class represents the main character in the game.
# This class extends the character class.
# This class adds an inventory that Luigi can use to obtain/store items.
# This class also adds an armor attribute that allows luigi to shield themselves from damage.
class luigi(character):
    
    def __init__(self):
        super().__init__("Luigi", 100, 1)
        self.inventory = {
                            "hearts":   {
                                            "smallHearts": [None] * ITEM_ARRAY_SIZE,
                                            "largeHearts": [None] * ITEM_ARRAY_SIZE
                                        },

                            "armor":    {
                                            "smallArmor": [None] * ITEM_ARRAY_SIZE,
                                            "largeArmor": [None] * ITEM_ARRAY_SIZE
                                        }
                        }
        self.armor = 0

    def addToInventory(self, item):
        luigi_funcs.placeInSlot(self, item)

    def getInventory(self):
        print("Inventory:")
        print("Hearts:")
        print("  Small Hearts: " + str(self.inventory["hearts"]["smallHearts"]))
        print("  Large Hearts: " + str(self.inventory["hearts"]["largeHearts"]))
        print("Armor:")
        print("  Small Armor: " + str(self.inventory["armor"]["smallArmor"]))
        print("  Large Armor: " + str(self.inventory["armor"]["largeArmor"]))

    # Separate function for adding health to Luigi.
    # Items that heal luigi will call this function to add health.
    def addHealth(self, amount):
        self.health = self.health + amount
        if self.health > 100:
            self.health = 100

    def takeDamage(self, amount):
        self.health = self.health - amount
        if self.health < 0:
            # TO-DO: Investigate if we can tie health to the game state
            # (i.e. if health is zero, then the game ends.)
            self.health = 0

    def vacuumAttack(self, enemy):
        ...# TO-DO: Implement vacuum attack functionality here

    def useSmallHeart(self):
        if self.inventory["hearts"]["smallHearts"] >= 1:
            self.addHealth(SMALL_HEART_HEALTH)
            self.inventory["hearts"]["smallHearts"] = self.inventory["hearts"]["smallHearts"] - 1
        else:
            print("No small hearts in inventory.")

    def useLargeHeart(self):
        if self.inventory["hearts"]["largeHearts"] >= 1:
            self.addHealth(LARGE_HEART_HEALTH)
            self.inventory["hearts"]["largeHearts"] = self.inventory["hearts"]["largeHearts"] - 1
        else:
            print("No large hearts in inventory.")


    # Before implementing armor functions, we should investigate how we want armor to work in this game.
    def useSmallArmor(self):
        if self.inventory["armor"]["smallArmor"] >= 1:
            # Equip one small armor to luigi's armor attribute
            self.armor = self.armor + SMALL_ARMOR_VALUE

            # Remove one small armor from the inventory
            self.inventory["armor"]["smallArmor"] = self.inventory["armor"]["smallArmor"] - 1
        else:
            print("No small armor in inventory.")

    def useLargeArmor(self):
        if self.inventory["armor"]["largeArmor"] >= 1:
            # Equip one large armor to luigi's armor attribute
            self.armor = self.armor + LARGE_ARMOR_VALUE

            # Remove one large armor from the inventory
            self.inventory["armor"]["largeArmor"] = self.inventory["armor"]["largeArmor"] - 1
        else:
            print("No large armor in inventory.")

    def useItem(self):
        self.getInventory();
        chosenItem = input("Please choose an item to use: \n1) Small Heart \n2) Large Heart \n3) Small Armor \n4) Large Armor: ")
        if chosenItem == "1":
            self.useSmallHeart()
        elif chosenItem == "2":
            self.useLargeHeart()
        elif chosenItem == "3":
            self.useSmallArmor()
        elif chosenItem == "4":
            self.useLargeArmor()
        else:
            print("Invalid choice. Please try again.")

    

    




    

