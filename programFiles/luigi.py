
# This is the luigi class.
# The luigi class extends the character class
# The luigi class adds an inventory to the character class that allows luigi to obtain/store items.
# The inventory is a dictionary that contains two dictionaries: one for hearts and one for armor.

import item, character

SMALL_HEART_HEALTH = 25
LARGE_HEART_HEALTH = 100

VACUUM_BASE_DAMAGE = 15


# This class represents the main character in the game.
# This class extends the character class.
# The addition to this class is an inventory that allows Luigi to obtain/store items.
class luigi(character):
    
    def __init__(self):
        super().__init__("Luigi", 100, 1)
        self.inventory = {
                            "hearts":   {
                                            "smallHearts": 0,
                                            "largeHearts": 0
                                        },

                            "armor":    {
                                            "smallArmor": 0,
                                            "largeArmor": 0
                                        }
                        }
        self.armor = 0;

    def addToInventory(self, item):
        if item.itemType == "smallHeart":
            self.inventory["hearts"]["smallHearts"] = self.inventory["hearts"]["smallHearts"] + 1
        elif item.itemType == "largeHeart":
            self.inventory["hearts"]["largeHearts"] = self.inventory["hearts"]["largeHearts"] + 1
        elif item.itemType == "smallArmor":
            self.inventory["armor"]["smallArmor"] = self.inventory["armor"]["smallArmor"] + 1
        elif item.itemType == "largeArmor":
            self.inventory["armor"]["largeArmor"] = self.inventory["armor"]["largeArmor"] + 1
        else:
            print("Item type not recognized. Item not added to inventory.")

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
        ... # TO-DO: Implement small armor functionality here

    def useLargeArmor(self):
        ... # TO-DO: Implement large armor functionality here        

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

    

    




    

