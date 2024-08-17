import copy
from dataclasses import dataclass
from enum import Enum

from .Items import SuitUpgrade

from .data.AreaNames import MetroidPrimeArea
from typing import TYPE_CHECKING, Dict

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
    # TODO: Standardize enums on snake case or CapitalCase
    SuitUpgrade.Power_Beam: DoorLockType.Power_Beam,
    SuitUpgrade.Wave_Beam: DoorLockType.Wave,
    SuitUpgrade.Ice_Beam: DoorLockType.Ice,
    SuitUpgrade.Plasma_Beam: DoorLockType.Plasma,
}


@dataclass
class AreaDoorTypeMapping:
    area: str
    type_mapping: Dict[str, str]

    def to_dict(self) -> Dict[str, Dict[str, str]]:
        return {
            "area": self.area,
            "type_mapping": self.type_mapping
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, str]]) -> 'AreaDoorTypeMapping':
        return cls(
            area=data['area'],
            type_mapping=data['type_mapping']
        )


def generate_random_door_color_mapping(world: 'MetroidPrimeWorld', area: MetroidPrimeArea) -> Dict[str, str]:
    shuffled_lock_types = get_available_lock_types(world, area)

    while True:
        world.random.shuffle(shuffled_lock_types)
        type_mapping = {original.value: new.value for original, new in zip(COLOR_LOCK_TYPES, shuffled_lock_types)}

        # Verify that no color matches its original color
        if all(original != new for original, new in type_mapping.items()):
            break

    return type_mapping


def get_world_door_mapping(world: 'MetroidPrimeWorld') -> Dict[str, AreaDoorTypeMapping]:
    door_type_mapping: Dict[str, AreaDoorTypeMapping] = {}

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
        bomb_door_area = world.random.choice([area for area in MetroidPrimeArea if area != world.starting_room_data.area and area != MetroidPrimeArea.Impact_Crater])
        replacement_color = world.random.choice(COLOR_LOCK_TYPES)
        door_type_mapping[bomb_door_area.value].type_mapping[replacement_color.value] = DoorLockType.Bomb.value

    return door_type_mapping


def get_available_lock_types(world: 'MetroidPrimeWorld', area: MetroidPrimeArea) -> list[DoorLockType]:
    locks = COLOR_LOCK_TYPES[:]
    if world.options.include_power_beam_doors:
        locks.append(DoorLockType.Power_Beam)
    return locks
