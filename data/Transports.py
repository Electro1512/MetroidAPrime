from typing import TYPE_CHECKING, Dict

from .RoomNames import RoomName
from .RoomData import MetroidPrimeArea
if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


default_elevator_mappings = {
    MetroidPrimeArea.Tallon_Overworld.value:
    {
        RoomName.Transport_to_Chozo_Ruins_West.value: RoomName.Transport_to_Tallon_Overworld_North.value,
        RoomName.Transport_to_Magmoor_Caverns_East.value: RoomName.Transport_to_Tallon_Overworld_West.value,
        RoomName.Transport_to_Chozo_Ruins_East.value: RoomName.Transport_to_Tallon_Overworld_East.value,
        RoomName.Transport_to_Chozo_Ruins_South.value: 'Chozo Ruins: ' + RoomName.Transport_to_Tallon_Overworld_South.value,
        RoomName.Transport_to_Phazon_Mines_East.value: 'Phazon Mines: ' + RoomName.Transport_to_Tallon_Overworld_South.value
    },
    MetroidPrimeArea.Chozo_Ruins.value:
    {
        RoomName.Transport_to_Tallon_Overworld_North.value: RoomName.Transport_to_Chozo_Ruins_West.value,
        RoomName.Transport_to_Magmoor_Caverns_North.value: RoomName.Transport_to_Chozo_Ruins_North.value,
        RoomName.Transport_to_Tallon_Overworld_East.value: RoomName.Transport_to_Chozo_Ruins_East.value,
        'Chozo Ruins: ' + RoomName.Transport_to_Tallon_Overworld_South.value: RoomName.Transport_to_Chozo_Ruins_South.value
    },
    MetroidPrimeArea.Magmoor_Caverns.value:
    {
        RoomName.Transport_to_Chozo_Ruins_North.value: RoomName.Transport_to_Magmoor_Caverns_North.value,
        RoomName.Transport_to_Phendrana_Drifts_North.value: RoomName.Transport_to_Magmoor_Caverns_West.value,
        RoomName.Transport_to_Tallon_Overworld_West.value: RoomName.Transport_to_Magmoor_Caverns_East.value,
        RoomName.Transport_to_Phendrana_Drifts_South.value: 'Phendrana Drifts: ' + RoomName.Transport_to_Magmoor_Caverns_South.value,
        RoomName.Transport_to_Phazon_Mines_West.value: 'Phazon Mines: ' + RoomName.Transport_to_Magmoor_Caverns_South.value
    },
    MetroidPrimeArea.Phendrana_Drifts.value:
    {
        RoomName.Transport_to_Magmoor_Caverns_West.value: RoomName.Transport_to_Phendrana_Drifts_North.value,
        'Phendrana Drifts: ' + RoomName.Transport_to_Magmoor_Caverns_South.value: RoomName.Transport_to_Phendrana_Drifts_South.value
    },
    MetroidPrimeArea.Phazon_Mines.value: {
        'Phazon Mines: ' + RoomName.Transport_to_Tallon_Overworld_South.value: RoomName.Transport_to_Phazon_Mines_East.value,
        'Phazon Mines: ' + RoomName.Transport_to_Magmoor_Caverns_South.value: RoomName.Transport_to_Phazon_Mines_West.value
    }
}


def temple_dest(boss) -> str:
    if boss == 0 or boss == 2:
        return "Crater Entry Point"
    else:
        return "Credits"


# Names of the transports that the config json expects
_transport_names_to_room_names: Dict[str, str] = {
    "Tallon Overworld North (Tallon Canyon)": RoomName.Transport_to_Chozo_Ruins_West.value,
    "Tallon Overworld West (Root Cave)": RoomName.Transport_to_Magmoor_Caverns_East.value,
    "Tallon Overworld East (Frigate Crash Site)": RoomName.Transport_to_Chozo_Ruins_East.value,
    "Tallon Overworld South (Great Tree Hall, Upper)": RoomName.Transport_to_Chozo_Ruins_South.value,
    "Tallon Overworld South (Great Tree Hall, Lower)": RoomName.Transport_to_Phazon_Mines_East.value,
    "Chozo Ruins West (Main Plaza)": RoomName.Transport_to_Tallon_Overworld_North.value,
    "Chozo Ruins North (Sun Tower)": RoomName.Transport_to_Magmoor_Caverns_North.value,
    "Chozo Ruins East (Reflecting Pool, Save Station)": RoomName.Transport_to_Tallon_Overworld_East.value,
    "Chozo Ruins South (Reflecting Pool, Far End)": "Chozo Ruins: " + RoomName.Transport_to_Tallon_Overworld_South.value,
    "Magmoor Caverns North (Lava Lake)": RoomName.Transport_to_Chozo_Ruins_North.value,
    "Magmoor Caverns West (Monitor Station)": RoomName.Transport_to_Phendrana_Drifts_North.value,
    "Magmoor Caverns East (Twin Fires)": RoomName.Transport_to_Tallon_Overworld_West.value,
    "Magmoor Caverns South (Magmoor Workstation, Save Station)": RoomName.Transport_to_Phendrana_Drifts_South.value,
    "Magmoor Caverns South (Magmoor Workstation, Debris)": RoomName.Transport_to_Phazon_Mines_West.value,
    "Phendrana Drifts North (Phendrana Shorelines)": RoomName.Transport_to_Magmoor_Caverns_West.value,
    "Phendrana Drifts South (Quarantine Cave)": "Phendrana Drifts: " + RoomName.Transport_to_Magmoor_Caverns_South.value,
    "Phazon Mines East (Main Quarry)": "Phazon Mines: " + RoomName.Transport_to_Tallon_Overworld_South.value,
    "Phazon Mines West (Phazon Processing Center)": "Phazon Mines: " + RoomName.Transport_to_Magmoor_Caverns_South.value,
}


def get_transport_name_by_room_name(room_name: str) -> str:
    for transport_name, room in _transport_names_to_room_names.items():
        if room == room_name:
            return transport_name
    return room_name


def get_room_name_by_transport_name(transport_name: str) -> str:
    return _transport_names_to_room_names.get(transport_name, transport_name)


def get_transport_data(world: 'MetroidPrimeWorld') -> Dict[str, Dict[str, str]]:
    mapping = world.elevator_mapping
    data = {}
    for area in world.elevator_mapping.keys():
        data[area] = {}
        for source, dest in mapping[area].items():
            data[area][get_transport_name_by_room_name(source)] = get_transport_name_by_room_name(dest)

    data[MetroidPrimeArea.Tallon_Overworld.value]["Artifact Temple"] = temple_dest(world.options.final_bosses)
    return data


def get_random_elevator_mapping(world: 'MetroidPrimeWorld') -> Dict[str, Dict[str, str]]:
    mapped_elevators = {area: {} for area in world.elevator_mapping.keys()}
    available_elevators_by_region = {**default_elevator_mappings}

    def get_region_with_most_unshuffled_elevators():
        max_elevators = 0
        region = None
        for area, elevators in available_elevators_by_region.items():
            num_elevators = len(elevators)
            if num_elevators > max_elevators:
                max_elevators = num_elevators
                region = area
        return region

    def get_random_target_region(source_region):
        target_regions = list(available_elevators_by_region.keys())
        target_regions.remove(source_region)
        return world.random.choice(target_regions)

    def delete_region_if_empty(region):
        if len(available_elevators_by_region[region]) == 0:
            del available_elevators_by_region[region]

    while len(available_elevators_by_region.keys()) > 0:
        source_region = get_region_with_most_unshuffled_elevators()
        source_elevators = available_elevators_by_region[source_region]
        source_elevator = world.random.choice(list(source_elevators.keys()))

        target_region = get_random_target_region(source_region)
        target_elevators = available_elevators_by_region[target_region]
        target_elevator = world.random.choice(list(target_elevators.keys()))

        mapped_elevators[source_region][source_elevator] = target_elevator
        mapped_elevators[target_region][target_elevator] = source_elevator

        # Remove the elevators from the available list
        del available_elevators_by_region[source_region][source_elevator]
        del available_elevators_by_region[target_region][target_elevator]

        # Check if the regions should be deleted
        delete_region_if_empty(source_region)
        delete_region_if_empty(target_region)
    return mapped_elevators
