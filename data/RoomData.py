from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional
import typing

from BaseClasses import CollectionState, ItemClassification, LocationProgressType, Region
from ..Items import ProgressiveUpgrade, SuitUpgrade
from ..Logic import can_bomb, can_ice_beam, can_missile, can_plasma_beam, can_wave_beam
from ..PrimeOptions import MetroidPrimeOptions
from ..data.AreaNames import MetroidPrimeArea
from ..Locations import METROID_PRIME_LOCATION_BASE, MetroidPrimeLocation, every_location
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


class DoorLockType(Enum):
    Blue = "Blue"
    Wave = "Wave Beam"
    Ice = "Ice Beam"
    Plasma = "Plasma Beam"
    Missile = "Missile"
    Bomb = "Bomb"
    None_ = "None"


@dataclass
class DoorData:
    defaultDestination: Optional[RoomName]
    defaultLock: DoorLockType = DoorLockType.Blue
    lock: Optional[DoorLockType] = None
    destination: Optional[RoomName] = None
    destinationArea: Optional[MetroidPrimeArea] = None  # Used for rooms that have the same name in different areas like Transport Tunnel A
    rule_func: Optional[Callable[[CollectionState, int], bool]] = None
    tricks: List[TrickInfo] = field(default_factory=list)
    exclude_from_rando: bool = False  # Used primarily for door rando when a door doesn't actually exist

    def get_destination_region_name(self):
        destination = self.destination.value if self.destination is not None else self.defaultDestination.value
        if self.destinationArea is not None:
            return f"{self.destinationArea.value}: {destination}"
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
    area: Optional[MetroidPrimeArea] = None  # Used for rooms that have duplicate names in different areas

    def get_config_data(self, world: 'MetroidPrimeWorld', parent_area: str):
        config = {
            "pickups": [pickup.get_config_data(world) for pickup in self.pickups if not pickup.exclude_from_config],
        }

        if world.options.door_color_randomization != "none":
            config["doors"] = self.get_door_config_data(world, parent_area)

        return config

    def get_door_config_data(self, world: 'MetroidPrimeWorld', parent_area: str):
        door_data = {}
        color_mapping: Dict[str, str] = world.options.door_color_mapping[parent_area].type_mapping
        for door_id, door in self.doors.items():
            if door.exclude_from_rando or door.defaultLock.value not in color_mapping:
                continue
            door_data[f"{door_id}"] = {
                "shieldType": door.lock.value if door.lock is not None else door.defaultLock.value,
            }
        return door_data

    def get_region_name(self, name: str):
        """Returns the name of the region, used primarily for rooms with duplicate names"""
        if self.area is not None:
            return f"{self.area.value}: {name}"
        return name


class AreaData:
    rooms: dict[RoomName, RoomData]
    area_name: str

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
        color_mapping: Dict[str, str] = world.options.door_color_mapping[self.area_name].type_mapping if world.options.door_color_randomization != "none" else {}
        for room_name, room_data in self.rooms.items():
            name = room_data.get_region_name(room_name.value)
            region = world.multiworld.get_region(name, world.player)
            for door_id, door_data in room_data.doors.items():
                destination = door_data.destination or door_data.defaultDestination
                if world.options.door_color_randomization != "none" and door_data.exclude_from_rando is False and door_data.defaultLock.value in color_mapping:
                    door_data.lock = DoorLockType(color_mapping[door_data.defaultLock.value])
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
    can_open = False
    lock = door_data.lock or door_data.defaultLock
    if lock is not None:
        if lock == DoorLockType.None_:
            can_open = True
        elif lock == DoorLockType.Blue:
            can_open = True
        elif lock == DoorLockType.Wave:
            can_open = can_wave_beam(state, player)
        elif lock == DoorLockType.Ice:
            can_open = can_ice_beam(state, player)
        elif lock == DoorLockType.Plasma:
            can_open = can_plasma_beam(state, player)
        elif lock == DoorLockType.Missile:
            can_open = can_missile(state, player)
        elif lock == DoorLockType.Bomb:
            can_open = can_bomb(state, player)
    else:
        can_open = True

    if not can_open:
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
