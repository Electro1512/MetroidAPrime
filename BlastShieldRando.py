from dataclasses import dataclass
from enum import Enum
import math
from .data.DoorData import get_door_data_by_room_names
from .data.BlastShieldRegions import get_valid_blast_shield_regions_by_area
from .data.RoomNames import RoomName
from .PrimeOptions import BlastShieldAvailableTypes, BlastShieldRandomization
from .data.AreaNames import MetroidPrimeArea
from typing import TYPE_CHECKING, Any, Dict, List

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
    Disabled = "Disabled"  # This is technically a door type, but functionally we want to add it the way that shields are added
    _None = "None"


@dataclass
class AreaBlastShieldMapping:
    area: str
    type_mapping: Dict[str, Dict[int, BlastShieldType]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "area": self.area,
            "type_mapping": {
                room: {door: shield.value for door, shield in doors.items()}
                for room, doors in self.type_mapping.items()
            }
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


MAX_BEAM_COMBO_DOORS_PER_AREA = 1
ALL_SHIELDS: List[BlastShieldType] = [shield for shield in BlastShieldType]
BEAM_COMBOS: List[BlastShieldType] = [BlastShieldType.Flamethrower, BlastShieldType.Ice_Spreader, BlastShieldType.Wavebuster]


def get_world_blast_shield_mapping(world: 'MetroidPrimeWorld') -> Dict[str, AreaBlastShieldMapping]:
    mapping: Dict[str, AreaBlastShieldMapping] = {}
    areas_with_locks = []
    if world.options.locked_door_count > 0:
        # No locks for magmoor since it is too linear and a central hub
        areas_with_locks = world.random.sample([area for area in list(MetroidPrimeArea) if area != MetroidPrimeArea.Magmoor_Caverns], world.options.locked_door_count)

    if world.options.blast_shield_randomization.value != BlastShieldRandomization.option_none:
        for area in MetroidPrimeArea:
            mapping[area.value] = AreaBlastShieldMapping(area.value, _generate_blast_shield_mapping_for_area(world, area, area in areas_with_locks))
    # Still generate mapping for areas with locks even if blast shields are disabled
    elif areas_with_locks:
        for area in areas_with_locks:
            mapping[area.value] = AreaBlastShieldMapping(area.value, _generate_blast_shield_mapping_for_area(world, area, True))
    return mapping


def _generate_blast_shield_mapping_for_area(world: 'MetroidPrimeWorld', area: MetroidPrimeArea, include_locked_door: bool) -> Dict[str, Dict[int, str]]:
    area_mapping: Dict[str, Dict[str, str]] = {}
    total_beam_combo_doors = 0
    # TODO: Make this less repetitive
    if world.options.blast_shield_randomization.value == BlastShieldRandomization.option_mix_it_up:
        blast_shield_regions = get_valid_blast_shield_regions_by_area(world, area)
        num_shields_to_add = math.ceil(world.options.blast_shield_frequency.value * len(blast_shield_regions) * .1)
        world.random.shuffle(blast_shield_regions)
        for i in range(num_shields_to_add):
            region = blast_shield_regions[i]
            source_room = world.random.choice(list(region.doors.keys()))
            _, door_id = get_door_data_by_room_names(source_room, region.doors[source_room], area, world)
            shield_type = world.random.choice(_get_available_blast_shields(world, total_beam_combo_doors >= MAX_BEAM_COMBO_DOORS_PER_AREA))
            if source_room.value not in area_mapping:
                area_mapping[source_room.value] = {}
            area_mapping[source_room.value][door_id] = shield_type

            if shield_type in BEAM_COMBOS:
                total_beam_combo_doors += 1

    elif world.options.blast_shield_randomization.value == BlastShieldRandomization.option_replace_existing:
        for room_name, room_data in world.game_region_data[area].rooms.items():
            for door_id, door_data in room_data.doors.items():
                if door_data.blast_shield:
                    if room_name.value not in area_mapping:
                        area_mapping[room_name.value] = {}

                    shield_type = world.random.choice(_get_available_blast_shields(world, total_beam_combo_doors >= MAX_BEAM_COMBO_DOORS_PER_AREA))
                    area_mapping[room_name.value][door_id] = shield_type

                    if shield_type in BEAM_COMBOS:
                        total_beam_combo_doors += 1

    if include_locked_door:
        lockable_regions = [regions for regions in get_valid_blast_shield_regions_by_area(world, area) if regions.can_be_locked]
        if lockable_regions:
            region = lockable_regions[0]
            source_room = world.random.choice(list(region.doors.keys()))
            _, door_id = get_door_data_by_room_names(source_room, region.doors[source_room], area, world)
            if source_room.value not in area_mapping:
                area_mapping[source_room.value] = {}
            area_mapping[source_room.value][door_id] = BlastShieldType.Disabled

    return area_mapping


def _get_available_blast_shields(world: 'MetroidPrimeWorld', force_exclude_combo_doors: bool = False) -> List[BlastShieldType]:
    available_shields = [shield for shield in ALL_SHIELDS.copy() if shield not in [BlastShieldType.Disabled, BlastShieldType._None]]
    if world.options.blast_shield_randomization.value == BlastShieldRandomization.option_replace_existing:
        available_shields.remove(BlastShieldType.Missile)

    if world.options.blast_shield_available_types.value == BlastShieldAvailableTypes.option_all and not force_exclude_combo_doors:
        return available_shields
    else:
        return [shield for shield in available_shields if shield not in BEAM_COMBOS]


def apply_blast_shield_mapping(world: 'MetroidPrimeWorld'):
    remove_vanilla_blast_shields(world)
    mapping = world.blast_shield_mapping
    for area, area_mapping in mapping.items():
        for room_name, door_mapping in area_mapping.type_mapping.items():
            for door_id, shield_type in door_mapping.items():
                world.game_region_data[MetroidPrimeArea(area)].rooms[RoomName(room_name)].doors[door_id].blast_shield = shield_type


def remove_vanilla_blast_shields(world: 'MetroidPrimeWorld'):
    for area in MetroidPrimeArea:
        for room_name, room_data in world.game_region_data[area].rooms.items():
            for door_id, door_data in room_data.doors.items():
                if door_data.blast_shield:
                    door_data.blast_shield = BlastShieldType._None
