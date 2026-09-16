


import json, sys
from level import level
from luigi import luigi

MAX_LEVEL_COUNT = 4


class game:
    def __init__(self):
        self.state = "EXPLORATION"
        self.isRunning = True
        self.player = luigi()
        self.currentLevelNumber = 1
        self.currentLevel = None
        self.currentRoomName = None
        self.activeGhost = None

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
                self.proccessCombatTurn()
            elif self.state == "GAME_OVER":
                print("\nYou got Ghosted! Game Over!")
                self.isRunning = False
            elif self.state == "VICTORY":
                print("\nCongratulations! You have now cleared the mansion!")
                self.isRunning = False

    def processExplorationState(self, currentRoom):

        print("\n--------------------------------------------------")
        print(f"Location: {currentRoom.roomName} (Floor {currentRoom.floor}) | Luigi HP: {self.player.health} | Armor: {self.player.armor}")
        print(currentRoom.getRoomDescription())

        print("\nObjects you can inspect:")
        for objectName, objectData in currentRoom.interactableObjects.items():
            status = "(Searched)" if objectData["isSearched"] else "(Unsearched)"
            print(f" - {objectName} {status}")
            
        # Get player input
        userInput = input("\nWhat would you like to do? (e.g., 'inspect [object]', 'move [room]', 'inventory', 'quit'): ").strip().lower()
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
                if outcome is not None and not isinstance(outcome, str):
                    self.activeGhost = outcome
                    self.state = "COMBAT"
                    print(f"\nA wild {self.activeGhost.getName()} appears! Prepare for battle!")
                    
                # Check if the outcome is an Item object / string 
                elif outcome is not None:
                    print(f"You found an item: {outcome}!")
                    # Use Luigi's built-in inventory routing method from luigi.py
                    self.player.addToInventory(outcome)
                    
            # Check if clearing this object finished the room
            if currentRoom.isCleared:
                print(f"\n* Click * The lights in {currentRoom.roomName} flicker on! The room is cleared.")
                self.checkLevelProgression()
                
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
            print("Unknown command. Try 'inspect [object]', 'move [room]', 'inventory', 'look', or 'quit'.")

    def processCombatTurn(self):
                print("\n*** BATTLE MODE ***")
                # TO-DO: Implement a function that will print to the screen an image of a ghost based on the ghost's name.
                #        Instantiate it here so that when a battle occurs the player can see what they are fighting.
                
                print(f"Luigi HP: {self.player.health} | Armor: {self.player.armor}")
                
                choice = input("Choose action: [1] Vacuum Attack [2] Run: ").strip()
                
                if choice == "1":
                    print("You flash the ghost with your Poltergust and pull!")
                    # TO-DO: Implement the vacuum attack method (it is currently unfinished in luigi.py)
                    #        # TO-DO: Implement a probability system that determines how much damage the ghost
                    #        # takes based on a variety of factors
                    # Trigger Luigi's vacuum attack once implemented
                    self.player.vacuumAttack(self.activeGhost)
                    self.activeGhost = None
                    self.state = "EXPLORATION"
                elif choice == "2":
                    # TO-DO: Implement a probability system for determining if Luigi can successfully escape the ghost's attack.
                    # - If successful, the ghost is tired and loses some of its health
                    # - if failed, the ghost attacks luigi first
                    print("You managed to scramble away! That ghost looks tired...")
                    self.activeGhost = None
                    self.state = "EXPLORATION"
                else:
                    print("Invalid choice.")
                

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
