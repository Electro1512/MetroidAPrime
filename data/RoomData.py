from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional
import typing

from BaseClasses import CollectionState, ItemClassification, LocationProgressType, Region
from ..BlastShieldRando import BlastShieldType
from ..DoorRando import DoorLockType
from ..Items import ProgressiveUpgrade, SuitUpgrade
from ..Logic import can_beam_combo, can_bomb, can_charge_beam, can_ice_beam, can_missile, can_plasma_beam, can_power_beam, can_power_bomb, can_super_missile, can_wave_beam
from ..PrimeOptions import MetroidPrimeOptions
from ..data.AreaNames import MetroidPrimeArea
from ..Locations import MetroidPrimeLocation, every_location
from .RoomNames import RoomName
from .Tricks import TrickInfo

if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld


def get_config_item_text(world: 'MetroidPrimeWorld', location) -> str:
    loc = world.multiworld.get_location(location, world.player)
    player_name = f"{world.multiworld.player_name[loc.item.player]}'s " if loc.item.player != world.player else ""
    return f"{player_name}{loc.item.name}"


def get_config_item_model(world: 'MetroidPrimeWorld', location) -> str:
    loc = world.multiworld.get_location(location, world.player)
    if loc.native_item:
        name = loc.item.name
        if name == SuitUpgrade.Missile_Expansion.value:
            return "Missile"
        elif name == SuitUpgrade.Missile_Launcher.value:
            return "Shiny Missile"
        elif name == SuitUpgrade.Main_Power_Bomb.value:
            return "Power Bomb"
        elif name == ProgressiveUpgrade.Progressive_Power_Beam.value or name == SuitUpgrade.Power_Beam.value:
            return "Super Missile"
        elif name == ProgressiveUpgrade.Progressive_Wave_Beam.value:
            return "Wave Beam"
        elif name == ProgressiveUpgrade.Progressive_Ice_Beam.value:
            return "Ice Beam"
        elif name == ProgressiveUpgrade.Progressive_Plasma_Beam.value:
            return "Plasma Beam"
        else:
            return name
    else:
        if loc.item.classification == ItemClassification.filler:
            return "Zoomer"
        elif loc.item.classification == ItemClassification.useful:
            return "Nothing"
        else:
            return "Cog"


@dataclass
class DoorData:
    default_destination: Optional[RoomName]
    defaultLock: DoorLockType = DoorLockType.Blue
    blast_shield: Optional[BlastShieldType] = None
    lock: Optional[DoorLockType] = None
    # TODO: Remove destination, not going to pursue room rando
    destination: Optional[RoomName] = None
    destination_area: Optional[MetroidPrimeArea] = None  # Used for rooms that have the same name in different areas like Transport Tunnel A
    rule_func: Optional[Callable[[CollectionState, int], bool]] = None
    tricks: List[TrickInfo] = field(default_factory=list)
    exclude_from_rando: bool = False  # Used primarily for door rando when a door doesn't actually exist

    def get_destination_region_name(self):
        destination = self.destination.value if self.destination is not None else self.default_destination.value
        if self.destination_area is not None:
            return f"{self.destination_area.value}: {destination}"
        return destination


@ dataclass
class PickupData:
    name: str
    rule_func: Optional[Callable[[CollectionState, int], bool]] = None
    tricks: List[TrickInfo] = field(default_factory=list)
    priority: LocationProgressType = LocationProgressType.DEFAULT
    exclude_from_config: bool = False  # Used when items need to be treated differently for logic with odd room connections
    exclude_from_logic: bool = False  # Used when items need to be treated differently for logic with odd room connections

    def get_config_data(self, world: 'MetroidPrimeWorld'):
        return {
            "type": "Unknown Item 1",
            "scanText": get_config_item_text(world, self.name),
            "hudmemoText": get_config_item_text(world, self.name) + " Acquired!",
            "currIncrease": 0,
            "model": get_config_item_model(world, self.name),
            "showIcon": True
        }


@ dataclass
class RoomData:
    doors: dict[int, DoorData] = field(default_factory=dict)
    pickups: list[PickupData] = field(default_factory=list)
    include_area_in_name: bool = False  # Used for rooms that have duplicate names in different areas
    area: Optional[MetroidPrimeArea] = None
    room_name: Optional[RoomName] = None

    def get_config_data(self, world: 'MetroidPrimeWorld', parent_area: str):
        config = {
            "pickups": [pickup.get_config_data(world) for pickup in self.pickups if not pickup.exclude_from_config],
        }

        config["doors"] = self.get_door_config_data(world, parent_area)

        return config

# TODO: Reduce duplication here w/ if/else. Make a single loop and operate on each door individually
# TODO: Make a test that verifies door rando output config so this will fail if it is not correct
    def get_door_config_data(self, world: 'MetroidPrimeWorld', parent_area: str):
        door_data = {}
        if world.door_color_mapping is not None:
            color_mapping: Dict[str, str] = world.door_color_mapping[parent_area].type_mapping
            for door_id, door in self.doors.items():
                if door.defaultLock.value not in color_mapping or not door.lock:
                    continue
                door_data[f"{door_id}"] = {
                    "shieldType": door.lock.value if door.lock is not None else door.defaultLock.value,
                }
        else:
            for door_id, door in self.doors.items():
                if door.lock is not door.defaultLock and door.lock is not None:
                    door_data[f"{door_id}"] = {
                        "shieldType": door.lock.value if door.lock is not None else door.defaultLock.value,
                    }

        for door_id, door in self.doors.items():
            if door.blast_shield is not None:
                if f"{door_id}" not in door_data:
                    door_data[f"{door_id}"] = {}
                door_data[f"{door_id}"]["blastShieldType"] = door.blast_shield.value

        return door_data

    def get_region_name(self, name: str):
        """Returns the name of the region, used primarily for rooms with duplicate names"""
        if self.include_area_in_name:
            return f"{self.area.value}: {name}"
        return name

    def get_matching_door(self, source_door: DoorData, world: 'MetroidPrimeWorld') -> Optional[DoorData]:
        target_room = world.game_region_data.get(self.area).rooms.get(source_door.default_destination)
        for door_data in target_room.doors.values():
            if door_data.default_destination == self.room_name:
                return door_data
        return None


class AreaData:
    def __init__(self, area_name: str):
        self.rooms: dict[RoomName, RoomData] = {}
        self.area_name: str = area_name

    def _init_room_names_and_areas(self):
        for room_name, room_data in self.rooms.items():
            room_data.room_name = room_name
            room_data.area = MetroidPrimeArea(self.area_name)

    def get_config_data(self, world: 'MetroidPrimeWorld'):
        return {
            name.value: data.get_config_data(world, self.area_name) for name, data in self.rooms.items()
        }

    def create_world_region(self, world: 'MetroidPrimeWorld'):
        # Create each room as a region
        for room_name, room_data in self.rooms.items():
            region_name = room_data.get_region_name(room_name.value)
            region = Region(region_name, world.player, world.multiworld)
            world.multiworld.regions.append(region)

            # Add each room's pickups as locations
            for pickup in room_data.pickups:
                if pickup.exclude_from_logic:
                    continue

                def generate_access_rule(pickup) -> Callable[[CollectionState], bool]:
                    def access_rule(state: CollectionState):
                        return _can_reach_pickup(state, world.player, pickup)
                    return access_rule

                region.add_locations({pickup.name: every_location[pickup.name]}, MetroidPrimeLocation)
                location = world.multiworld.get_location(pickup.name, world.player)
                location.access_rule = generate_access_rule(pickup)

        # Once each region is created, connect the doors and assign their locks
        color_mapping: Dict[str, str] = world.door_color_mapping[self.area_name].type_mapping if world.options.door_color_randomization != "none" else {}
        for room_name, room_data in self.rooms.items():
            name = room_data.get_region_name(room_name.value)
            region = world.multiworld.get_region(name, world.player)
            for door_id, door_data in room_data.doors.items():
                destination = door_data.destination or door_data.default_destination
                if world.options.door_color_randomization != "none" and door_data.exclude_from_rando is False and door_data.defaultLock.value in color_mapping:
                    door_data.lock = DoorLockType(color_mapping[door_data.defaultLock.value])

                paired_door = room_data.get_matching_door(door_data, world)
                if paired_door is not None and paired_door.blast_shield is not None:
                    door_data.blast_shield = paired_door.blast_shield
                elif door_data.blast_shield is not None:
                    paired_door.blast_shield = door_data.blast_shield

                if destination is None:
                    continue

                def generate_rule_func(door_data) -> Callable[[CollectionState], bool]:
                    def rule_func(state: CollectionState):
                        return _can_access_door(state, world.player, door_data)
                    return rule_func

                lock = door_data.lock or door_data.defaultLock
                target_region = world.multiworld.get_region(door_data.get_destination_region_name(), world.player)
                region.connect(target_region, f"{lock.value} Door from {name} to {destination.value}", generate_rule_func(door_data))


def _get_options(state: CollectionState, player: int) -> MetroidPrimeOptions:
    return state.multiworld.worlds[player].options


def _can_reach_pickup(state: CollectionState, player: int, pickup_data: PickupData) -> bool:
    """Determines if the player is able to reach the pickup based on their items and selected trick difficulty"""
    max_difficulty = _get_options(state, player).trick_difficulty.value
    allow_list = _get_options(state, player).trick_allow_list
    deny_list = _get_options(state, player).trick_deny_list
    for trick in pickup_data.tricks:
        if trick.name not in allow_list and (trick.difficulty.value > max_difficulty or trick.name in deny_list):
            continue
        elif trick.rule_func is not None and trick.rule_func(state, player):
            return True

    if pickup_data.rule_func is None:
        return True
    elif pickup_data.rule_func(state, player):
        return True
    return False


def _can_access_door(state: CollectionState, player: int, door_data: DoorData) -> bool:
    """Determines if the player can open the door based on the lock type as well as whether they can reach it or not"""
    max_difficulty = _get_options(state, player).trick_difficulty.value
    allow_list = _get_options(state, player).trick_allow_list
    deny_list = _get_options(state, player).trick_deny_list
    can_color = False
    can_blast_shield = False
    lock = door_data.lock or door_data.defaultLock
    if lock is not None:
        if lock == DoorLockType.None_:
            can_color = True
        elif lock == DoorLockType.Blue:
            can_color = True
        elif lock == DoorLockType.Wave:
            can_color = can_wave_beam(state, player)
        elif lock == DoorLockType.Ice:
            can_color = can_ice_beam(state, player)
        elif lock == DoorLockType.Plasma:
            can_color = can_plasma_beam(state, player)
        elif lock == DoorLockType.Power_Beam:
            can_color = can_power_beam(state, player)
        elif lock == DoorLockType.Missile:
            can_color = can_missile(state, player)
        elif lock == DoorLockType.Bomb:
            can_color = can_bomb(state, player)
    else:
        can_color = True

    if door_data.blast_shield is not None:
        if door_data.blast_shield == BlastShieldType.Bomb:
            can_blast_shield = can_bomb(state, player)
        elif door_data.blast_shield == BlastShieldType.Missile:
            can_blast_shield = can_missile(state, player)
        elif door_data.blast_shield == BlastShieldType.Power_Bomb:
            can_blast_shield = can_power_bomb(state, player)
        elif door_data.blast_shield == BlastShieldType.Charge_Beam:
            can_blast_shield = can_charge_beam(state, player)
        elif door_data.blast_shield == BlastShieldType.Super_Missile:
            can_blast_shield = can_super_missile(state, player)
        elif door_data.blast_shield == BlastShieldType.Wavebuster:
            can_blast_shield = can_beam_combo(state, player, SuitUpgrade.Wave_Beam)
        elif door_data.blast_shield == BlastShieldType.Ice_Spreader:
            can_blast_shield = can_beam_combo(state, player, SuitUpgrade.Ice_Beam)
        elif door_data.blast_shield == BlastShieldType.Flamethrower:
            can_blast_shield = can_beam_combo(state, player, SuitUpgrade.Plasma_Beam)
    else:
        can_blast_shield = True

    if not can_color or not can_blast_shield:
        return False

    for trick in door_data.tricks:
        if trick.name in allow_list:
            pass
        if trick.name not in allow_list and (trick.difficulty.value > max_difficulty or trick.name in deny_list):
            continue
        elif trick.rule_func is not None and trick.rule_func(state, player):
            return True
    if door_data.rule_func is None:
        return True
    elif door_data.rule_func(state, player):
        return True

    return False
