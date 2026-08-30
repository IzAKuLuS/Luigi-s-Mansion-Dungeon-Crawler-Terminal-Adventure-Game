
import item, character


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

    def displayInventory(self):
        print("Inventory:")
        print("Hearts:")
        print("  Small Hearts: " + str(self.inventory["hearts"]["smallHearts"]))
        print("  Large Hearts: " + str(self.inventory["hearts"]["largeHearts"]))
        print("Armor:")
        print("  Small Armor: " + str(self.inventory["armor"]["smallArmor"]))
        print("  Large Armor: " + str(self.inventory["armor"]["largeArmor"]))

    




    

