


import json, sys
from level import level
from luigi import luigi
from ghost import ghost
from item import item

MAX_LEVEL_COUNT = 4

4
class game:
    def __init__(self, player=None):
        self.state = "EXPLORATION"
        self.isRunning = True
        self.player = player if player is not None else luigi()
        self.currentLevelNumber = 1
        self.currentLevel = None
        self.currentRoomName = None
        self.activeGhost = None
        self.activeGhostObjectName = None
        self.saveId = None

    # This function initializes the game and loads the first level
    def start(self):
        # Print the game welcome message
        print("==================================================")
        print("      LUIGI'S MANSION: TERMINAL ADVENTURE         ")
        print("==================================================")

        self.loadLevel(self.currentLevelNumber)

    # This function loads the level blueprints from the associated JSON file and initializes the level object
    def loadLevel(self, levelNumber):
        #TO-DO: Create the JSON files that contain the rooms for each level
        fileName = f"level_{levelNumber}_rooms.json"

        # try to open the JSON file and load the level data
        try:
            with open(fileName, "r") as file:
                data = json.load(file)
                levelName = data["levelName"]
                roomBlueprints = data["rooms"]
                numGhosts = data["numGhosts"]
                numItems = data["numItems"]

                self.currentLevel = level(levelName, roomBlueprints, numGhosts, numItems)

                self.currentRoomName = list(self.currentLevel.rooms.keys())[0]
                print(f"\n[Entering Floor {levelNumber}: {self.currentLevel.levelName}]")
        except FileNotFoundError:
            print(f"Error: Level {levelNumber} file not found.")
            self.isRunning = False

    def runGameLoop(self):
        while self.isRunning:

            currentRoom = self.currentLevel.rooms[self.currentRoomName]

            if self.player.health <= 0:
                self.state = "GAME_OVER"


            if self.state == "EXPLORATION":
                self.processExplorationState(currentRoom)
            elif self.state == "COMBAT":
                self.processCombatTurn()
            elif self.state == "GAME_OVER":
                print("\nYou got Ghosted! Game Over!")
                self.isRunning = False
            elif self.state == "VICTORY":
                print("\nCongratulations! You have now cleared the mansion!")
                self.isRunning = False

    def processExplorationState(self, currentRoom):

        print("\n--------------------------------------------------")
        print(
            f"Location: {currentRoom.roomName} (Floor {currentRoom.floor}) | "
            f"{self.player.name} HP: {self.player.health} | "
            f"Armor: {self.player.getArmorStatus()}"
        )
        print(currentRoom.getRoomDescription())

        print("\nObjects you can inspect:")
        for objectName, objectData in currentRoom.interactableObjects.items():
            status = "(Searched)" if objectData["isSearched"] else "(Unsearched)"
            print(f" - {objectName} {status}")
            
        # Get player input
        userInput = input(
            "\nWhat would you like to do? "
            "(e.g., 'inspect [object]', 'move [room]', 'inventory', "
            "'use [item]', 'save', 'quit'): "
        ).strip().lower()
        parts = userInput.split(" ", 1)
        
        verb = parts[0] if len(parts) > 0 else ""
        noun = parts[1] if len(parts) > 1 else ""
        
        # Command Parsing
        if verb == "quit":
            print("Exiting game. Goodbye!")
            self.isRunning = False
        
        # Loops back to print room details    
        elif verb == "look":
            pass 
            
        elif verb == "inventory":
            self.player.getInventory()

        elif verb == "use":
            if not noun:
                print("Specify an item to use.")
                return
            self.player.useInventoryItem(noun)

        elif verb == "save":
            self.save()
            
        elif verb == "inspect":
            if not noun:
                print("Specify an object.")
                
            # Call the inspectObject method from the room class
            result = currentRoom.inspectObject(noun)
            print(f"\n{result['message']}")
            
            # Handle outcome if something was found successfully
            if result["status"] == "success":
                outcome = result["outcome"]
                
                # Check if the outcome is a Ghost object (not a string or None)
                if isinstance(outcome, ghost):
                    self.activeGhost = outcome
                    self.activeGhostObjectName = noun
                    self.state = "COMBAT"
                    print(f"\nA wild {self.activeGhost.getName()} appears! Prepare for battle!")
                    
                # Check if the outcome is an Item object / string 
                elif isinstance(outcome, item):
                    print(f"You found an item: {outcome.name}!")
                    # Use Luigi's built-in inventory routing method from luigi.py
                    self.player.addToInventory(outcome)
                    
            # Check if clearing this object finished the room
            if (
                result["status"] == "success"
                and currentRoom.isCleared
                and self.state != "COMBAT"
            ):
                self.completeClearedRoom(currentRoom)
                
        elif verb == "move" or verb == "go":
            if not noun:
                print("Specify a room name.")
                return
                
            targetRoom = noun.title()
            if targetRoom in self.currentLevel.rooms:
                self.currentRoomName = targetRoom
                print(f"You walk into the {targetRoom}.")
            else:
                print(f"You cannot reach '{noun}' from here or it doesn't exist. Try again.")
        else:
            print(
                "Unknown command. Try 'inspect [object]', 'move [room]', "
                "'inventory', 'use [item]', 'save', 'look', or 'quit'."
            )

    def processCombatTurn(self):
        if self.activeGhost is None:
            self.state = "EXPLORATION"
            return

        print("\n*** BATTLE MODE ***")
        print(
            f"{self.player.name} HP: {self.player.health} | "
            f"Armor: {self.player.getArmorStatus()} | "
            f"{self.activeGhost.name} HP: {self.activeGhost.health}"
        )

        choice = input(
            "Choose action: [1] Vacuum Attack [2] Run "
            "[3] Use Item [4] Save [5] Inventory: "
        ).strip().lower()

        if choice in {"4", "save"}:
            self.save()
            return

        if choice in {"5", "inventory"}:
            self.player.getInventory()
            return

        if choice == "3":
            requestedItem = input("Which item would you like to use? ").strip()
            itemWasUsed = self.player.useInventoryItem(requestedItem)
            if itemWasUsed:
                self.processGhostCounterattack()
            return

        if choice.startswith("use "):
            requestedItem = choice.split(" ", 1)[1]
            itemWasUsed = self.player.useInventoryItem(requestedItem)
            if itemWasUsed:
                self.processGhostCounterattack()
            return

        if choice in {"1", "attack", "vacuum", "vacuum attack"}:
            print("You flash the ghost with your Poltergust and pull!")
            self.player.attack(self.activeGhost)

            if self.activeGhost.health <= 0:
                defeated_ghost_name = self.activeGhost.name
                print(f"You captured the {defeated_ghost_name}!")
                self.finishCombat()
                return

            self.processGhostCounterattack()

        elif choice in {"2", "run", "flee"}:
            print("You managed to scramble away! The ghost returns to its hiding spot.")
            self.returnGhostToHidingSpot()
            self.activeGhost = None
            self.activeGhostObjectName = None
            self.state = "EXPLORATION"
        else:
            print("Invalid choice.")

    def processGhostCounterattack(self):
        """Allow the active ghost to attack after the player's turn."""
        if self.activeGhost is None or self.activeGhost.health <= 0:
            return

        print(f"The {self.activeGhost.name} counterattacks!")
        self.activeGhost.attack(self.player)

        if self.player.health <= 0:
            self.state = "GAME_OVER"

    def finishCombat(self):
        """End a won battle and process any resulting room completion."""
        currentRoom = self.currentLevel.rooms[self.currentRoomName]
        hidingSpotName = getattr(self, "activeGhostObjectName", None)

        if hidingSpotName in currentRoom.interactableObjects:
            currentRoom.interactableObjects[hidingSpotName]["outcome"] = None

        currentRoom.isRoomCleared()

        self.activeGhost = None
        self.activeGhostObjectName = None
        self.state = "EXPLORATION"

        if currentRoom.isCleared:
            self.completeClearedRoom(currentRoom)

    def returnGhostToHidingSpot(self):
        """Make a fled encounter available to discover and fight again."""
        currentRoom = self.currentLevel.rooms[self.currentRoomName]
        hidingSpotName = getattr(self, "activeGhostObjectName", None)

        if hidingSpotName in currentRoom.interactableObjects:
            currentRoom.interactableObjects[hidingSpotName]["isSearched"] = False
            currentRoom.isCleared = False

    def completeClearedRoom(self, currentRoom):
        print(f"\n* Click * The lights in {currentRoom.roomName} flicker on! The room is cleared.")
        self.checkLevelProgression()

    def save(self, filePath=None):
        """Save the current game into its existing save slot."""
        # Imported here to avoid the module-level game/game_funcs import cycle.
        from game_funcs import SaveFileError, save_game

        previousSaveId = getattr(self, "saveId", None)
        try:
            self.saveId = save_game(
                self,
                save_id=previousSaveId,
                file_path=filePath,
            )
        except (SaveFileError, TypeError) as error:
            self.saveId = previousSaveId
            print(f"Unable to save the game: {error}")
            return False

        print(f"Game saved successfully in save #{self.saveId}.")
        return True
                

    def checkLevelProgression(self):

        allRoomsClear = all(r.isCleared for r in self.currentLevel.rooms.values())

        if allRoomsClear:
            print(f"\n***LEVEL {self.currentLevelNumber} COMPLETE! ***")
            self.currentLevelNumber += 1

            if self.currentLevelNumber > MAX_LEVEL_COUNT:
                self.state = "VICTORY"

            else:
                print("A key drops from the ceiling! I wonder where this leads to?")
                self.loadLevel(self.currentLevelNumber)
