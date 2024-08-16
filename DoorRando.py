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
    Power_Beam = "Power Beam"
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
