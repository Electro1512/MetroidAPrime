import copy
from dataclasses import dataclass
from enum import Enum

from .data.RoomNames import RoomName

from .Items import SuitUpgrade

from .data.AreaNames import MetroidPrimeArea
from typing import TYPE_CHECKING, Callable, Dict, List, TypedDict

if TYPE_CHECKING:
    from . import MetroidPrimeWorld


class DoorLockType(Enum):
    Blue = "Blue"
    Wave = "Wave Beam"
    Ice = "Ice Beam"
    Plasma = "Plasma Beam"
    Missile = "Missile"
    Power_Beam = "Power Beam Only"
    Bomb = "Bomb"
    None_ = "None"


COLOR_LOCK_TYPES = [
    # DoorLockType.Blue, # this requires some extra logic
    DoorLockType.Wave,
    DoorLockType.Ice,
    DoorLockType.Plasma,
]

BEAM_TO_LOCK_MAPPING = {
    SuitUpgrade.Power_Beam: DoorLockType.Power_Beam,
    SuitUpgrade.Wave_Beam: DoorLockType.Wave,
    SuitUpgrade.Ice_Beam: DoorLockType.Ice,
    SuitUpgrade.Plasma_Beam: DoorLockType.Plasma,
}


class AreaDoorTypeMappingDict(TypedDict):
    area: str
    type_mapping: Dict[str, str]


@dataclass
class AreaDoorTypeMapping:
    area: str
    type_mapping: Dict[str, str]

    def to_dict(self) -> AreaDoorTypeMappingDict:
        return {
            "area": self.area,
            "type_mapping": self.type_mapping
        }

    @classmethod
    def from_dict(cls, data: AreaDoorTypeMappingDict) -> 'AreaDoorTypeMapping':
        return cls(
            area=data['area'],
            type_mapping=data['type_mapping']
        )


class WorldDoorMapping(Dict[str, AreaDoorTypeMapping]):
    def to_option_value(self) -> Dict[str, AreaDoorTypeMappingDict]:
        return {area: mapping.to_dict() for area, mapping in self.items()}

    @classmethod
    def from_option_value(cls, data: Dict[str, AreaDoorTypeMappingDict]) -> 'WorldDoorMapping':
        return WorldDoorMapping({area: AreaDoorTypeMapping.from_dict(mapping) for area, mapping in data.items()})


def generate_random_door_color_mapping(world: 'MetroidPrimeWorld', area: MetroidPrimeArea) -> Dict[str, str]:
    shuffled_lock_types = get_available_lock_types(world, area)

    def is_valid_mapping(mapping: Dict[str, str]) -> bool:
        return all(original != new for original, new in mapping.items())

    # Can't start w/ Ice beam when fighting Thardus
    def is_valid_mapping_for_quarantine_monitor(mapping: Dict[str, str]) -> bool:
        return is_valid_mapping(mapping) and mapping[DoorLockType.Wave.value] != DoorLockType.Ice.value

    validate_func: Callable[[Dict[str, str]], bool] = lambda mapping: is_valid_mapping(mapping)

    if world.starting_room_data and world.starting_room_data.name == RoomName.Quarantine_Monitor.value:
        validate_func = is_valid_mapping_for_quarantine_monitor

    while True:
        world.random.shuffle(shuffled_lock_types)
        type_mapping = {original.value: new.value for original, new in zip(COLOR_LOCK_TYPES, shuffled_lock_types)}

        # Verify that no color matches its original color
        if validate_func(type_mapping):
            break

    return type_mapping


def get_world_door_mapping(world: 'MetroidPrimeWorld') -> WorldDoorMapping:
    door_type_mapping: Dict[str, AreaDoorTypeMapping] = {}

    assert world.starting_room_data is not None

    if world.options.door_color_randomization == 'global':
        global_mapping = generate_random_door_color_mapping(world, world.starting_room_data.area)

        for area in MetroidPrimeArea:
            door_type_mapping[area.value] = AreaDoorTypeMapping(area.value, copy.deepcopy(global_mapping))

    else:
        for area in MetroidPrimeArea:
            mapping = generate_random_door_color_mapping(world, area)
            door_type_mapping[area.value] = AreaDoorTypeMapping(area.value, mapping)

    # Add Bomb doors to a random area if they are enabled
    if world.options.include_morph_ball_bomb_doors:
        bomb_door_area = world.random.choice([area for area in MetroidPrimeArea if area != world.starting_room_data.area])
        replacement_color = world.random.choice(COLOR_LOCK_TYPES)
        door_type_mapping[bomb_door_area.value].type_mapping[replacement_color.value] = DoorLockType.Bomb.value

    return WorldDoorMapping(door_type_mapping)


def get_available_lock_types(world: 'MetroidPrimeWorld', area: MetroidPrimeArea) -> List[DoorLockType]:
    locks = COLOR_LOCK_TYPES[:]
    # If start beam is randomized, we replace whatever the mapping to starting beam is with Power Beam Only
    if world.options.include_power_beam_doors and not world.options.randomize_starting_beam:
        locks.append(DoorLockType.Power_Beam)
    return locks


# This needs to take place after the starting beam is initialized
def remap_doors_to_power_beam_if_necessary(world: 'MetroidPrimeWorld'):
    if world.options.include_power_beam_doors and world.door_color_mapping:
        assert world.starting_room_data is not None and world.starting_room_data.selected_loadout is not None
        starting_beam = world.starting_room_data.selected_loadout.starting_beam

        if starting_beam is not SuitUpgrade.Power_Beam:
            for area, mapping in world.door_color_mapping.items():
                if area == world.starting_room_data.area.value and world.starting_room_data.no_power_beam_door_on_starting_level:
                    continue
                for original, new in mapping.type_mapping.items():
                    if new == BEAM_TO_LOCK_MAPPING[starting_beam].value:
                        world.door_color_mapping[area].type_mapping[original] = DoorLockType.Power_Beam.value
            world.options.door_color_mapping.value = world.door_color_mapping.to_option_value()
