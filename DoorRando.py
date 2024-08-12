from dataclasses import dataclass

from .data.RoomData import DoorLockType
from .data.AreaNames import MetroidPrimeArea
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from . import MetroidPrimeWorld

COLOR_LOCK_TYPES = [
    # DoorLockType.Blue,
    DoorLockType.Wave,
    DoorLockType.Ice,
    DoorLockType.Plasma,
]


@dataclass
class AreaDoorTypeMapping:
    area: str
    type_mapping: Dict[str, str]


def generate_random_door_color_mapping(world: 'MetroidPrimeWorld') -> Dict[str, str]:
    shuffled_lock_types = COLOR_LOCK_TYPES[:]

    while True:
        world.random.shuffle(shuffled_lock_types)
        type_mapping = {original.value: new.value for original, new in zip(COLOR_LOCK_TYPES, shuffled_lock_types)}

        # Verify that no color matches its original color
        if all(original != new for original, new in type_mapping.items()):
            break

    return type_mapping


def get_world_door_mapping(world: 'MetroidPrimeWorld') -> dict[MetroidPrimeArea, AreaDoorTypeMapping]:
    door_type_mapping = {}
    global_mapping = None
    if world.options.door_color_randomization == 'global':
        global_mapping = generate_random_door_color_mapping(world)

    for area in MetroidPrimeArea:
        mapping = global_mapping if global_mapping else generate_random_door_color_mapping(world)
        door_type_mapping[area.value] = AreaDoorTypeMapping(area.value, mapping)
    return door_type_mapping
