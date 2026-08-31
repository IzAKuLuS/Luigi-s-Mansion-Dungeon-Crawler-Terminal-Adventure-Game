

import luigi

SMALL_HEART_HEALTH = 25
LARGE_HEART_HEALTH = 100

SMALL_ARMOR_VALUE = 1
LARGE_ARMOR_VALUE = 3


def placeInSlot(luigi, item):
    if item.itemType == "smallHeart":
        for i in range(len(luigi.inventory["hearts"]["smallHearts"])):
            if luigi.inventory["hearts"]["smallHearts"][i] is None:
                luigi.inventory["hearts"]["smallHearts"][i] = item
                break;
        print("No empty slots available for small hearts.")

    elif item.itemType == "largeHeart":
        for i in range(len(luigi.inventory["hearts"]["largeHearts"])):
            if luigi.inventory["hearts"]["largeHearts"][i] is None:
                luigi.inventory["hearts"]["largeHearts"][i] = item
                break;
        print("No empty slots available for large hearts.")
        

    elif item.itemType == "smallArmor":
        for i in range(len(luigi.inventory["armor"]["smallArmor"])):
            if luigi.inventory["armor"]["smallArmor"][i] is None:
                luigi.inventory["armor"]["smallArmor"][i] = item
                break;
        print("No empty slots available for small armor.")
        
    elif item.itemType == "largeArmor":
        for i in range(len(luigi.inventory["armor"]["largeArmor"])):
            if luigi.inventory["armor"]["largeArmor"][i] is None:
                luigi.inventory["armor"]["largeArmor"][i] = item
                break;
        print("No empty slots available for large armor.")
        
    else:
        print("Invalid item type.")

