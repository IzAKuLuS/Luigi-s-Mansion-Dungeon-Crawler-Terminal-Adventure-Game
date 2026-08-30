





# This class represents a character.
# Each character contains within it a name, a health level, an inventory, and a skill.
# Name and health are self explanatory (I hope...)
# Inventory consists of a dictionary of dictionaries. Each sub dictionary holds specific items within the larger dictionary
# Skill represents a number that is used to determine the amount of damage one can do. 
class character:
    def __init__(self, name, health, inventory, skill):
        self.name = name
        self.health = health
        self.inventory = {

                "hearts": {
                    
                    },
                "armor": {

                    }

                }
        self.skill = skill


