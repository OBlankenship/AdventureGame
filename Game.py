from art import *
import csv


class Item:
    def __init__(self, name, pickup, description, is_open, key):
        self._name = name
        self._pickup = pickup
        self._description = description
        self._is_open = is_open
        self._key = key

    def get_description(self):
        return self._description

    def can_pickup(self):
        return self._pickup


class Room:
    def __init__(self, name, description1, description2, items, connections):
        self._name = name
        self._description1 = description1
        self._description2 = description2
        self._connections = connections
        self._items = items
        self._visited = 0

    def get_connections(self):
        return self._connections

    def get_description(self):
        if self._visited == 0:
            self._visited = 1
            return self._description1
        else:
            return self._description2

    def look_around(self):
        print(self._description1)

    def get_name(self):
        return self._name

    def get_items(self):
        return self._items

    def remove_item(self, item):
        self._items.pop(item)

    def add_item(self, item):
        self._items.append(item)


class Player:
    def __init__(self, location):
        self._health = 100
        self._location = location
        self._inventory = []

    def get_health(self):
        return self._health

    def get_location(self):
        return self._location

    def get_inventory(self):
        return self._inventory

    def set_location(self, location):
        self._location = location

    def set_health(self, health):
        self._health = health

    def add_inventory(self, item):
        self._inventory.append(item)

    def remove_inventory(self, item):
        self._inventory.remove(item)


def lookup_room(room):
    return room_dict[room]


def go(direction):
    current_location = player.get_location()
    connections = current_location.get_connections()
    if connections[direction] == "None":
        print("You can't go that way!")
    else:
        next_location = lookup_room(connections[direction])
        player.set_location(next_location)
        print(next_location.get_description())


def display_help():
    print("HELP".center(80, '*'))
    print("Recognized Verbs Include:\n"
          "Go\n"
          "Take\n"
          "Look\n")


def print_inventory():
    inventory = player.get_inventory()
    print("You currently have the following items:")
    if len(inventory) == 0:
        print("Nothing!")
    for item in inventory:
        print(item)


def player_action():
    direction_list = ["NORTH", "EAST", "SOUTH", "WEST", "UP", "DOWN"]
    next_action = input("What do you do?: ")
    next_word = next_action.split()
    location = player.get_location()
    items = location.get_items()

    if len(next_word) == 0:
        print("Invalid command!")

    elif next_word[0].upper() == "HELP":
        display_help()

    elif next_word[0].upper() == "INVENTORY":
        print_inventory()

    elif len(next_word) == 1:
        print("Invalid command!")

    elif next_word[0].upper() == "GO":
        direction = next_word[1].upper()
        if direction in direction_list:
            go(direction)
        else:
            print("Not a direction! Must go a cardinal direction or up/down.")

    elif next_word[0].upper() == "LOOK":
        if next_word[1].upper() == "AROUND":
            location.look_around()
            return None
        elif next_word[1].upper() == "AT" and len(next_word) > 2:
            item = next_word[2].upper()
        else:
            item = next_word[1].upper()
        if item in items:
            print(items[item].get_description())
        else:
            print("There is no " + item + " here!")

    elif next_word[0].upper() == "TAKE":
        item = next_word[1].upper()
        if item in items and items[item].can_pickup() == "YES":
            location.remove_item(item)
            player.add_inventory(item)
        elif item in items and items[item].can_pickup() == "NO":
            print("You can't pick up the " + next_word[1] + "!")
        else:
            print("You don't see a " + next_word[1] + " here")

    else:
        print("Invalid command!")


def generate_items(name):
    with open("items.csv", "r") as data_file:
        data = csv.reader(data_file, delimiter=",")
        headers = next(data)[1:]
        item_dict = {}
        for row in data:
            if row[0] == name:
                item_name = row[1]
                pickup = row[2]
                description = row[3]
                is_open = row[4]
                key = row[5]
                item_dict[item_name] = Item(item_name, pickup, description, is_open, key)
        return item_dict


def generate_rooms():
    room_dict = {}
    with open("rooms.csv", "r") as data_file:
        data = csv.reader(data_file, delimiter=",")
        headers = next(data)[1:]
        for row in data:
            name = row[0]
            description1 = row[1]
            description2 = row[2]
            connections = row[3].split(" ")
            connections_dict = {}
            connections_dict["NORTH"] = connections[0]
            connections_dict["EAST"] = connections[1]
            connections_dict["SOUTH"] = connections[2]
            connections_dict["WEST"] = connections[3]
            connections_dict["UP"] = connections[4]
            connections_dict["DOWN"] = connections[5]
            items = generate_items(name)
            room_dict[name] = Room(name, description1, description2, items, connections_dict)
    return room_dict


def game_init():
    tprint("Welcome", "calgphy2")
    aprint("sword")
    print("You are in a darkened cell. There is a door to the north, and a bed.")
    room_dict = generate_rooms()
    return room_dict


room_dict = game_init()
player = Player(room_dict["CELL"])
while player.get_health() > 0:
    player_action()
