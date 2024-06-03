import json
import os
import sys


def get_room_data():
    """Returns the room data from the RoomNames.json file"""
    file_name = "RoomNames"
    file_path = os.path.join(os.path.dirname(__file__), 'data', file_name)
    with open(file_path + ".json", "r") as f:
        return json.load(f)


def get_level_data():
    file_name = "LevelData"
    file_path = os.path.join(os.path.dirname(__file__), 'data', file_name)
    with open(file_path + ".json", "r") as f:
        return json.load(f)


def room_to_enum(room_name):
    """Converts a room name to the enum name"""
    return "RoomName." + room_name.replace(" ", "_").replace(":", "_").replace("\'", "")


nl = "\n"
t = "\t"


def convert_rooms_enum():
    """Converts the RoomNames.json file to a RoomNamesEnum.json file with keys that are valid enum names to convert to a python enum"""
    data = get_room_data()
    new_data = {}
    for key in data:
        # Skip frigate intro rooms
        if "Orpheon" in key:
            continue
        new_value = key.split(':')[1]
        new_key = new_value.replace(" ", "_").replace(":", "_").replace("'", "")
        new_data[new_key] = new_value
    new_file = """
from enum import Enum


class RoomName(Enum):
"""
    for key in new_data:
        new_file += f'\t\t{key} = "{new_data[key]}"\n'
    write_path = os.path.join(os.path.dirname(__file__), "RoomNames.py")
    with open(write_path, "w") as f:
        f.write(new_file)


def convert_config_py():
    """Converts the Config.py files levelData contents to use the enum"""
    from worlds.metroidprime.data.RoomNames import RoomName
    file_name = "config.py"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    data_str = ""
    with open(file_path, "r") as f:
        data_str = f.read()

    for room in RoomName:
        new_str = f"RoomName.{room.name}"
        old_str = f"\"{room.value}\""
        print(f"{old_str} -> {new_str}")
        data_str = data_str.replace(old_str, new_str)
    with open(file_path, "w") as f:
        f.write(data_str)


def create_prime_areas():
    """Goes through each line in the roomnames.json, looks for the associated data in config.py, and adds its pickups to the area"""
    room_data = get_room_data()
    level_data = get_level_data()
    area_data = {}

    def get_door_str() -> str:
        return "{}"

    def get_room_row(room) -> str:
        pickup_str = ""
        pickups = room["pickups"]
        for pickup in pickups:
            pickup_str += f"PickupData('{pickup['name']}', required_items=[], tricks=[]), "

        return f"RoomData(doors={get_door_str()}, pickups=[{pickup_str}])"

    for room in room_data:
        [area, original_room_name] = room.split(":")
        room_name = room_to_enum(original_room_name)
        if area not in area_data:
            area_data[area] = {}

        if room_name not in area_data[area]:
            area_data[area][room_name] = {"doors": {}, "pickups": []}

        config_data = level_data[area]["rooms"][original_room_name]
        if "pickups" in config_data:
            for pickup in config_data["pickups"]:
                area_data[area][room_name]["pickups"].append(
                    {"name": area + ": " + pickup["scanText"]}
                )
        if config_data == None:
            print(f"Config data not found for {room}")
            continue
    for area in area_data:
        area_name = area.replace(" ", "")
        file_str = f"""
from .RoomData import AreaData, PickupData, RoomData
from .RoomNames import RoomName


class {area_name}AreaData(AreaData):
    rooms = {"{"}
{f",{nl}".join([f"        {room}: {get_room_row(area_data[area][room])}" for room in area_data[area]])}
    {"}"}
"""
        with open(os.path.join(os.path.dirname(__file__), "data", area_name + ".py"), "w") as f:
            f.write(file_str)
            # json.dump(area_data[area], f, indent=4)


if __name__ == "__main__":
    # check for args to determine if we call convert rooms
    if len(sys.argv) > 1:
        if sys.argv[1] == "rooms":
            print("Converting RoomNames.json to RoomNames.py")
            convert_rooms_enum()
        elif sys.argv[1] == "config":
            print("Converting Config.py to use RoomNamesEnum")
            convert_config_py()
        elif sys.argv[1] == "areas":
            print("Creating area data")
            create_prime_areas()
