import json
import os
import sys


def convert_rooms_enum():
    """Converts the RoomNames.json file to a RoomNamesEnum.json file with keys that are valid enum names to convert to a python enum"""
    file_name = "RoomNames"
    file_path = os.path.join(os.path.dirname(__file__), 'data', file_name)
    new_data = {}
    with open(file_path + ".json", "r") as f:
        data = json.load(f)
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
    write_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(write_path + ".py", "w") as f:
        f.write(new_file)


def convert_config_py():
    """Converts the Config.py files levelData contents to use the enum"""
    from RoomNames import RoomName
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

    # for each value in the room name enum, search for it in the string and replace it with the enum name

    # with open(file_path, "w") as f:
    #     f.write("config = " + str(new_data))


if __name__ == "__main__":
    # check for args to determine if we call convert rooms
    if len(sys.argv) > 1:
        if sys.argv[1] == "rooms":
            print("Converting RoomNames.json to RoomNames.py")
            convert_rooms_enum()
        elif sys.argv[1] == "config":
            print("Converting Config.py to use RoomNamesEnum")
            convert_config_py()
