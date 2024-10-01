
# Name :  Attia Inayat
# Roll no: SP23-BAI-012

# map of castle
rooms = {
    "entrance": {
        "description": "You are at the entrance of the castle. Massive wooden doors creak behind you. To the north is the grand hall.",
        "exits": {"north": "grand_hall"},
        "items": [],
        "puzzle": {},
    },
    "grand_hall": {
        "description": "You are in the grand hall. Exits lead south (entrance), north(kitchen), east (library), and west (basement)",
        "exits": {
            "south": "entrance",
            "east": "library",
            "west": "basement",
            "north": "kitchen",
        },
        "items":["torch"],
        "puzzle": {},
    },
    "library": {
        "description": "You are in the library. There is too much dark here .To the west(grand hall)",
        "exits": {"west": "grand_hall"},
        "items": ["book"], 
        "puzzle": {"light_room": False, "solve_riddle": False},
    },
    "kitchen": {
        "description": "You are in the kitchen. You can see a lever here to press. To the south (grand hall) ",
        "exits": {"south": "grand_hall"},
        "items": ["lever"],
        "puzzle": {"press_lever": False, "open_exit_door": False},
    },
    "basement": {
        "description": "You are in the basement now. To the east there is a grand hall.",
        "exits": {"east": "grand_hall"},
        "items": ["key"],
        "puzzle": {"door_locked": False},
    },
}

# variables to track the current room and player's inventory
current_room = "entrance"
inventory = []


# displays the current room and its items
def look():
    print(rooms[current_room]["description"])
    if rooms[current_room]["items"]:
        print(
            f"You can see the following items in { current_room }: {','.join(rooms[current_room]['items'])}"
        )


# to move in a direction
def move(direction):
    global current_room
    # check if the direction exist in current room direction
    if direction in rooms[current_room]["exits"]:
        # checks if it is basement
        if rooms[current_room]["exits"][direction] == "basement":
            # checks if the door is locked
            if rooms["basement"]["puzzle"]["door_locked"] == False:
                print("You can't go that way.You first have to unlock the door. ")
                return

        # other cases
        current_room = rooms[current_room]["exits"][direction]
        look()

    else:
        print("You cannot go that way.")


# to take an item
def take(item):
    if item in rooms[current_room]["items"]:
        inventory.append(item)
        rooms[current_room]["items"].remove(item)
        print(f"{item} is added in your inventory")

    else:
        print(f"{item} is not present in this room")


# to drop an item
def drop(item):
    if item in inventory:
        inventory.remove(item)
        rooms[current_room]["items"].append(item)
        print(
            f" {item} is dropped from your inventory to your current room {current_room}"
        )
    else:
        print(f"{item} is not present in your inventory.")


# to use an item in a specific room
def use_item(item):

    # to light up the library
    if item == "torch" and current_room == "library":
        rooms[current_room]["puzzle"]["light_room"] = True
        rooms[current_room][
            "description"
        ] = "You are in the library . There you see a book on pedestal."
        print(f" Your puzzle light_room is solved now. and the library is lighten up")
    # to solve the riddle in book
    elif (
        item == "book"
        and current_room == "library"
        and rooms[current_room]["puzzle"]["light_room"] == True
    ):
        solve_riddle()
    # to press the lever
    elif item == "key" and current_room == "kitchen":
        rooms[current_room]["puzzle"]["press_lever"] = True
        print("The lever has been pressed")
    # open the exit door
    elif item == "lever" and current_room == "kitchen":
        rooms[current_room]["puzzle"]["open_exit_door"] = True
        print("Hurrayy! You have unlocked the exit door")
        print("You can now leave the castle and end the game. Type 'quit' to exit.")
        
    else:
        print(f"You can't use {item} here.")


# to examine an object
def examine(object):
    if object == "torch":
        print("Torch is used to lighten up the library. type (use torch) command in library")
    elif object == "lever":
        print(" lever will open the exit door")
    elif object == "key":
        print( "key is used to press the lever in kitchen")
    elif object == "book":
        print("By solving the riddle on book you can open the basement door. type (use book) command for the riddle. ")
    else:
        print(f"There is no information about {object}")


# solve the riddle in book that is in the library
def solve_riddle():
    print(
        "Riddle: I have cities but no houses. I have mountains but no trees. I have water but no fish. What am I?"
    )
    answer = input("Your answer :   ").lower()
    if answer == "map":
        rooms["library"]["puzzle"]["solve_riddle"] = True
        rooms["basement"]["puzzle"]["door_locked"] = True
        print("Your answer is correct. You have unlocked the basement door")
    else:
        print("Wrong answer! Please try again")


# save the game in file
def save_game():
    file = open("game.txt", "w")
    file.write(f"{current_room}\n")
    file.write(",".join(inventory))
    file.close()
    print("game saved")


# load current room and inventory from file
def load_game():
    global current_room, inventory #recontinuing the game from where we have saved last time
    try:
        with open("game.txt") as f:
            current_room = f.readline().strip()
            inventory = f.readline().strip().split(",")
            print("Game loaded")
            print("Current Room: ", current_room)
            print("Inventory: ", inventory)
    except FileNotFoundError:
        print("Your file does not found")


def display_help():
    """Displays available commands."""
    print(
        """
Available commands:
- go [direction] : Move in a direction (north, south, east, west, etc.)
- look : Redisplay the current room's description
- take [item] : Pick up an item from the room
- drop [item] : Drop an item from your inventory
- use [item] : Use an item in the room
- examine [item] : Will give the details about a specific object 
- inventory : View your current items
- save : Save the current game state
- load : Load a previously saved game
- quit : Exit the game
- help : Display available commands
"""
    )


def main():

    print("Welcome to the mysterious Castle Adventure")
    look()

    while True:
        command = input("What would you like to do? ").lower().split()
        if len(command) == 0:  # check if the command is valid or not
            print("Invalid command .Try again")
            continue

        # otherwise process commands
        action = command[0]
        if action == "quit":
            print("Thanks for playing ")
            break
        # to move in a direction
        elif action == "go":
            if len(command) > 1:
                move(command[1])
            else:
                print("Go where? ")

        # to take an item
        elif action == "take":
            if len(command) > 1:
                take(command[1])
            else:
                print("Take what ? ")

        # to drop an item
        elif action == "drop":
            if len(command) > 1:
                drop(command[1])
            else:
                print("Drop what ? ")

        # to look
        elif action == "look":
            look()

        # to use
        elif action == "use":
            if len(command) > 1:
                use_item(command[1])
            else:
                print("Use what ? ")

        # to examine an object
        elif action == "examine":
            if len(command) > 1:
                examine(command[1])
            else:
                print("Examine what ? ")

        # to see your inventory
        elif action == "inventory":
            print(f" Your inventory is {','.join(inventory) if inventory else 'empty'}")

        # to save game to file
        elif action == "save":
            save_game()

        # to load game from file
        elif action == "load":
            load_game()

        # to see all list of commands
        elif action == "help":
            display_help()

        # invalid command
        else:
            print("Invalid command. Type 'help' for a list of commands.")


if __name__ == "__main__":
    main()
