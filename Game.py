class Room:
    def __init__(self, name, description1, description2, connections):
        self._name = name
        self._description1 = description1
        self._description2 = description2
        self._connections = connections
        self._visited = 0

    def get_connections(self):
        return self._connections

    def get_description(self):
        if self._visited == 0:
            return self._description1
        else:
            self._visited = 1
            return self._description2

    def get_name(self):
        return self._name


class Player:
    def __init__(self, location):
        self._health = 100
        self._location = location
        self._inventory = []

    def get_health(self):
        return self._health

    def get_location(self):
        return self._location

    def set_location(self, location):
        self._location = location

    def set_health(self, health):
        self._health = health

    def add_inventory(self, item):
        self._inventory.append(item)

    def remove_inventory(self, item):
        self._inventory.remove(item)


def go(direction):
    current_location = player.get_location()
    connections = current_location.get_connections()
    if connections[direction] is None:
        print("You can't go that way!")
    else:
        next_location = lookup_room(connections[direction])
        player.set_location(next_location)
        print(next_location.get_description())


def lookup_room(room):
    for entry in room_list:
        if entry.get_name() == room:
            return entry


def player_action():
    direction_list = ["NORTH", "EAST", "SOUTH", "WEST", "UP", "DOWN"]
    while player.get_health() > 0:
        next_action = input("What do you do?: ")
        next_word = next_action.split()
        if next_word[0].upper() == "GO":
            direction = next_word[1].upper()
            if direction in direction_list:
                go(direction)
            else:
                print("Not a direction! Must go a cardinal direction or up/down.")
        else:
            print("Invalid command!")


def game_init():
    room_list = []

    cell = Room("cell",
                "You are in a darkened cell. You hear the faint sound of dripping water.",
                "You are in the cell where you awoke.",
                {"NORTH": "dungeon", "EAST": None, "SOUTH": None, "WEST": None, "UP": None, "DOWN": None})
    room_list.append(cell)

    dungeon = Room("dungeon",
                   "You are in a dungeon. There are cells to the south, east, and west. There is a metal door "
                   "to the north.",
                   "You are in the dungeon.",
                   {"NORTH": None, "EAST": None, "SOUTH": "cell", "WEST": None, "UP": None, "DOWN": None})
    room_list.append(dungeon)

    print("You awaken in a dark room. You can hear water dripping from the ceiling.")
    return room_list


room_list = game_init()
player = Player(lookup_room("cell"))
player_action()
