
# This is the luigi class.
# The luigi class extends the character class
# The luigi class adds an inventory to the character class that allows luigi to obtain/store items.
# The inventory is a dictionary that contains two dictionaries: one for hearts and one for armor.

from item import item
from character import character

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

    def placeInSlot(self, foundItem):
        inventoryLocations = {
            "smallHeart": ("hearts", "smallHearts"),
            "largeHeart": ("hearts", "largeHearts"),
            "smallArmor": ("armor", "smallArmor"),
            "largeArmor": ("armor", "largeArmor"),
        }
        location = inventoryLocations.get(foundItem.itemType)

        if location is None:
            print("Invalid item type.")
            return False

        category, itemType = location
        slots = self.inventory[category][itemType]

        for index, storedItem in enumerate(slots):
            if storedItem is None:
                slots[index] = foundItem
                return True

        print(f"No empty slots available for {foundItem.name}.")
        return False

    def addToInventory(self, foundItem):
        return self.placeInSlot(foundItem)

    @staticmethod
    def normalizeItemName(itemName):
        return "".join(character for character in itemName.lower() if character.isalnum())

    def findInventoryItem(self, requestedName):
        """Find an inventory item by its display name or item type."""
        normalizedRequest = self.normalizeItemName(requestedName)

        for category in self.inventory.values():
            for slots in category.values():
                for index, storedItem in enumerate(slots):
                    if storedItem is None:
                        continue

                    validNames = {
                        self.normalizeItemName(storedItem.name),
                        self.normalizeItemName(storedItem.itemType),
                        self.normalizeItemName(storedItem.name + "s"),
                    }
                    if normalizedRequest in validNames:
                        return storedItem, slots, index

        return None

    def useInventoryItem(self, requestedName):
        """Use a named inventory item and remove it when it is consumed."""
        inventoryEntry = self.findInventoryItem(requestedName)
        if inventoryEntry is None:
            print(f"You do not have '{requestedName}' in your inventory.")
            return False

        inventoryItem, slots, index = inventoryEntry
        if self.useItem(inventoryItem):
            slots[index] = None
            return True

        return False

    def getInventory(self):
        print("\nInventory:")
        print()
        print("Hearts:")
        print("  Small Hearts: " + self.describeItemSlots("hearts", "smallHearts"))
        print("  Large Hearts: " + self.describeItemSlots("hearts", "largeHearts"))
        print("Armor:")
        print("  Small Armor: " + self.describeArmorSlots("smallArmor"))
        print("  Large Armor: " + self.describeArmorSlots("largeArmor"))
        print("\nUse an item with 'use [item name]'.\n")

    def describeItemSlots(self, category, itemType):
        descriptions = [
            storedItem.name if storedItem is not None else "Empty"
            for storedItem in self.inventory[category][itemType]
        ]
        return str(descriptions)

    def describeArmorSlots(self, armorType):
        descriptions = []
        for armorItem in self.inventory["armor"][armorType]:
            if armorItem is None:
                descriptions.append("Empty")
            else:
                descriptions.append(
                    f"{armorItem.name} ({armorItem.durability} hits remaining)"
                )
        return str(descriptions)

    def findActiveArmor(self):
        """Return the first usable armor item and its inventory location."""
        defaultDurability = {"smallArmor": 3, "largeArmor": 5}

        for armorType in ("smallArmor", "largeArmor"):
            slots = self.inventory["armor"][armorType]
            for index, armorItem in enumerate(slots):
                if armorItem is None:
                    continue

                # Supply durability when loading an older save created before
                # armor durability was introduced.
                if not hasattr(armorItem, "durability"):
                    armorItem.durability = defaultDurability[armorType]

                if armorItem.durability < 1:
                    slots[index] = None
                    continue

                return armorItem, slots, index

        return None

    def getArmorStatus(self):
        activeArmor = self.findActiveArmor()
        if activeArmor is None:
            return "None"

        armorItem, _, _ = activeArmor
        return f"{armorItem.name} ({armorItem.durability} hits remaining)"

    # Separate function for adding health to Luigi.
    # Items that heal luigi will call this function to add health.
    def addHealth(self, amount):
        self.health = self.health + amount
        if self.health > 100:
            self.health = 100

    def takeDamage(self, amount):
        activeArmor = self.findActiveArmor()
        damage = amount

        if activeArmor is not None:
            armorItem, slots, index = activeArmor
            damage = (amount + 1) // 2
            armorItem.durability -= 1
            print(
                f"{armorItem.name} reduces the incoming damage from "
                f"{amount} to {damage}."
            )

            if armorItem.durability < 1:
                print(f"{armorItem.name} has broken and was removed from your inventory.")
                slots[index] = None

        return super().takeDamage(damage)

    def attack(self, enemy):
        """Attack an enemy with the Poltergust vacuum."""
        return self.vacuumAttack(enemy)

    def vacuumAttack(self, enemy):
        """Damage an enemy with Luigi's Poltergust."""
        damage = VACUUM_BASE_DAMAGE * self.skill
        enemy.takeDamage(damage)
        print(f"{self.name} vacuums {enemy.name} for {damage} damage!")
        return damage

    def useItem(self, inventoryItem):
        """Apply an item's effect using its itemType and magnitude."""
        if inventoryItem.itemType in {"smallHeart", "largeHeart"}:
            if self.health >= 100:
                print("Your health is already full.")
                return False

            previousHealth = self.health
            self.addHealth(inventoryItem.magnitude)
            restoredHealth = self.health - previousHealth
            print(
                f"You used {inventoryItem.name} and restored "
                f"{restoredHealth} health."
            )
            return True

        if inventoryItem.itemType in {"smallArmor", "largeArmor"}:
            print(
                f"{inventoryItem.name} is equipped automatically and has "
                f"{inventoryItem.durability} hits remaining."
            )
            return False

        print(f"{inventoryItem.name} cannot be used.")
        return False

    

    
    
    




    
