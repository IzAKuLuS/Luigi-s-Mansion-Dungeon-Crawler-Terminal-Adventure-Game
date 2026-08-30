

class item:
    def __init__(self, name, description, itemType):
        self.name = name
        self.description = description
        self.itemType = itemType

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getItemType(self):
        return self.itemType

    def setName(self, name):
        self.name = name;

    def setDescription(self, description):
        self.description = description

    def setItemType(self, itemType):
        self.itemType = itemType
