from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List

from .data.RoomNames import RoomName

from .PrimeOptions import BlastShieldAvailableTypes, BlastShieldRandomization

from .data.AreaNames import MetroidPrimeArea

if TYPE_CHECKING:
    from . import MetroidPrimeWorld


class BlastShieldType(Enum):
    Bomb = "Bomb"
    Charge_Beam = "Charge Beam"
    Flamethrower = "Flamethrower"
    Ice_Spreader = "Ice Spreader"
    Wavebuster = "Wavebuster"
    Power_Bomb = "Power Bomb"
    Super_Missile = "Super Missile"
    Missile = "Missile"

@dataclass
class AreaBlastShieldMapping:
    area: str
    type_mapping: Dict[str, Dict[int, str]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "area": self.area,
            "type_mapping": self.type_mapping
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AreaBlastShieldMapping':
        mapping = cls(
            area=data['area'],
            type_mapping=data['type_mapping']
        )

        for room, doors in mapping.type_mapping.items():
            mapping.type_mapping[room] = {int(door): BlastShieldType(shield) for door, shield in doors.items()}

        return mapping


def get_world_blast_shield_mapping(world: 'MetroidPrimeWorld') -> Dict[str, AreaBlastShieldMapping]:
    mapping: Dict[str, AreaBlastShieldMapping] = {}
    if world.options.blast_shield_randomization.value != BlastShieldRandomization.option_none:
        for area in MetroidPrimeArea:
            mapping[area.value] = AreaBlastShieldMapping(area.value, _generate_blast_shield_mapping_for_area(world, area))
    return mapping


def _generate_blast_shield_mapping_for_area(world: 'MetroidPrimeWorld', area: MetroidPrimeArea) -> Dict[str, Dict[int, str]]:
    area_mapping: Dict[str, Dict[str, str]] = {}

    if world.options.blast_shield_randomization.value != BlastShieldRandomization.option_replace_existing:
        return area_mapping

    for room_name, room_data in world.game_region_data[area].rooms.items():
        for door_id, door_data in room_data.doors.items():
            if door_data.blast_shield:
                if room_name.value not in area_mapping:
                    area_mapping[room_name.value] = {}
                area_mapping[room_name.value][door_id] = world.random.choice(_get_available_blast_shields(world))

    return area_mapping


def _get_available_blast_shields(world: 'MetroidPrimeWorld') -> List[BlastShieldType]:
    all_shields: List[BlastShieldType] = [shield for shield in BlastShieldType]
    beam_combos: List[BlastShieldType] = [BlastShieldType.Flamethrower, BlastShieldType.Ice_Spreader, BlastShieldType.Wavebuster]

    if world.options.blast_shield_randomization.value == BlastShieldRandomization.option_replace_existing:
        all_shields.remove(BlastShieldType.Missile)

    if world.options.blast_shield_available_types.value == BlastShieldAvailableTypes.option_all:
        return all_shields
    elif world.options.blast_shield_available_types.value == BlastShieldAvailableTypes.option_no_beam_combos:
        return [shield for shield in all_shields if shield not in beam_combos]
    else:
        return [BlastShieldType.Missile]


def apply_blast_shield_mapping(world: 'MetroidPrimeWorld'):
    mapping = world.blast_shield_mapping
    for area, area_mapping in mapping.items():
        for room_name, door_mapping in area_mapping.type_mapping.items():
            for door_id, shield_type in door_mapping.items():
                world.game_region_data[MetroidPrimeArea(area)].rooms[RoomName(room_name)].doors[door_id].blast_shield = shield_type
