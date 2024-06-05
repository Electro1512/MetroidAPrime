from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional
import typing

from BaseClasses import CollectionState, Region
from worlds.metroidprime.Items import SuitUpgrade
from worlds.metroidprime.PrimeOptions import MetroidPrimeOptions

from ..Locations import METROID_PRIME_LOCATION_BASE, MetroidPrimeLocation, every_location
from .RoomNames import RoomName
from .Tricks import TrickInfo

if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld


def get_config_item_text(world, location) -> str:
    loc = world.multiworld.get_location(location, world.player)
    player_name = f"{world.multiworld.player_name[loc.item.player]}'s " if loc.item.player != world.player else ""
    return f"{player_name}{loc.item.name}"


def get_config_item_model(world, location) -> str:
    loc = world.multiworld.get_location(location, world.player)
    if loc.native_item:
        name = loc.item.name
        if name == "Missile Expansion":
            return "Missile"
        elif name == "Missile Launcher":
            return "Shiny Missile"
        elif name == "Power Bomb (Main)":
            return "Power Bomb"
        else:
            return name
    else:
        return "Nothing"


class MetroidPrimeArea(Enum):
    Phendrana_Drifts = "Phendrana Drifts"
    Chozo_Ruins = "Chozo Ruins"
    Magmoor_Caverns = "Magmoor Caverns"
    Tallon_Overworld = "Tallon Overworld"
    Phazon_Mines = "Phazon Mines"
    Impact_Crater = "Impact Crater"


class Capabilities(Enum):
    Can_Boost = "Can Boost"
    Can_Bomb = "Can Bomb"
    Can_Power_Bomb = "Can Power Bomb"
    Can_Spider = "Can Spider"
    Can_Missile = "Can Missile"
    Can_Super_Missile = "Can Super Missile"
    Can_Wave_Beam = "Can Wave Beam"
    Can_Ice_Beam = "Can Ice Beam"
    Can_Plasma_Beam = "Can Plasma Beam"
    Can_Melt_Ice = "Can Melt Ice"
    Can_Grapple = "Can Grapple"
    Can_Space_Jump = "Can Space Jump"
    Can_Morph_Ball = "Can Morph Ball"
    Can_XRay = "Can XRay"
    Can_Thermal = "Can Thermal"
    Can_Move_Underwater = "Can Move Underwater"
    Can_Charge_Beam = "Can Charge Beam"
    Cannot_Reach = "Cannot Reach"  # Used for doors that are impossible to reach without tricks


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
    required_items: List[typing.Union[Capabilities, List[Capabilities]]] = field(default_factory=list)  # If multiple lists are present, it will treat each group as a separate OR
    rule_func: Optional[Callable[[CollectionState, int], bool]] = None
    tricks: List[TrickInfo] = field(default_factory=list)

    def get_config_data(self, world: 'MetroidPrimeWorld'):
        return {
            "type": "Unknown Item 1",
            "scanText": get_config_item_text(world, self.name),
            "hudmemoText": get_config_item_text(world, self.name) + " Acquired!",
            "currIncrease": every_location[self.name] - METROID_PRIME_LOCATION_BASE + 1,
            "model": get_config_item_model(world, self.name),
            "showIcon": True
        }


@ dataclass
class RoomData:
    doors: dict[int, DoorData] = field(default_factory=dict)
    pickups: list[PickupData] = field(default_factory=list)
    area: Optional[MetroidPrimeArea] = None  # Used for rooms that have duplicate names in different areas

    def get_config_data(self, world: 'MetroidPrimeWorld'):
        if len(self.pickups) == 0:
            return {}
        return {
            "pickups": [pickup.get_config_data(world) for pickup in self.pickups],
        }

    def get_region_name(self, name: str):
        """Returns the name of the region, used primarily for rooms with duplicate names"""
        if self.area is not None:
            return f"{self.area.value}: {name}"
        return name


class AreaData:
    rooms: dict[RoomName, RoomData]

    def get_config_data(self, world: 'MetroidPrimeWorld'):
        return {
            name.value: data.get_config_data(world) for name, data in self.rooms.items()
        }

    def create_world_region(self, world: 'MetroidPrimeWorld'):
        # Create each room as a region
        for room_name, room_data in self.rooms.items():
            region_name = room_data.get_region_name(room_name.value)
            region = Region(region_name, world.player, world.multiworld)
            world.multiworld.regions.append(region)

            # Add each room's pickups as locations
            for pickup in room_data.pickups:
                def generate_access_rule(pickup) -> Callable[[CollectionState], bool]:
                    def access_rule(state: CollectionState):
                        return _can_reach_pickup(state, world.player, pickup)
                    return access_rule

                region.add_locations({pickup.name: every_location[pickup.name]}, MetroidPrimeLocation)
                location = world.multiworld.get_location(pickup.name, world.player)
                location.access_rule = generate_access_rule(pickup)

        # Once each region is created, connect the doors
        for room_name, room_data in self.rooms.items():
            name = room_data.get_region_name(room_name.value)
            region = world.multiworld.get_region(name, world.player)
            for door_id, door_data in room_data.doors.items():
                destination = door_data.destination or door_data.defaultDestination
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

    for trick in pickup_data.tricks:
        if trick.difficulty.value > max_difficulty:
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
    can_open = False
    lock = door_data.lock or door_data.defaultLock
    if lock is not None:
        if lock == DoorLockType.None_:
            can_open = True
        elif lock == DoorLockType.Blue:
            can_open = True
        elif lock == DoorLockType.Wave:
            can_open = state.has(SuitUpgrade.Wave_Beam.value, player)
        elif lock == DoorLockType.Ice:
            can_open = state.has(SuitUpgrade.Ice_Beam.value, player)
        elif lock == DoorLockType.Plasma:
            can_open = state.has(SuitUpgrade.Plasma_Beam.value, player)
        elif lock == DoorLockType.Missile:
            can_open = state.has(SuitUpgrade.Missile_Launcher.value, player)
        elif lock == DoorLockType.Bomb:
            can_open = state.has(SuitUpgrade.Morph_Ball_Bomb.value, player)
    else:
        can_open = True

    if not can_open:
        return False

    for trick in door_data.tricks:
        if trick.difficulty.value > max_difficulty:
            continue
        elif trick.rule_func is not None and trick.rule_func(state, player):
            return True
    if door_data.rule_func is None:
        return True
    elif door_data.rule_func(state, player):
        return True

    return False
