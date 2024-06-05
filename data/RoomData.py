from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional
import typing

from BaseClasses import CollectionState

from ..Locations import METROID_PRIME_LOCATION_BASE, every_location
from .RoomNames import RoomName
from .Tricks import Trick_Type, TrickDifficulty, TrickInfo

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
    lock: Optional[DoorLockType]
    destination: Optional[RoomName]
    destinationArea: Optional[MetroidPrimeArea]  # Used for rooms that have the same name in different areas like Transport Tunnel A
    # deprecated, going to move towards rules_func instead
    rule_func: Optional[Callable[[CollectionState, int], bool]] = None
    tricks: List[TrickInfo] = []
    exclude_from_rando: bool = False  # Used primarily for door rando when a door doesn't actually exist


@ dataclass
class PickupData:
    name: str
    required_items: List[typing.Union[Capabilities, List[Capabilities]]] = []  # If multiple lists are present, it will treat each group as a separate OR
    rule_func: Optional[Callable[[CollectionState, int], bool]] = None
    tricks: List[TrickInfo] = []

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
    doors: dict[int, DoorData] = {}
    pickups: list[PickupData] = []
    area: Optional[MetroidPrimeArea] = None  # Used for rooms that have duplicate names in different areas

    def get_config_data(self, world: 'MetroidPrimeWorld'):
        if len(self.pickups) == 0:
            return {}
        return {
            "pickups": [pickup.get_config_data(world) for pickup in self.pickups],
        }


class AreaData:
    rooms: dict[RoomName, RoomData]

    def get_config_data(self, world: 'MetroidPrimeWorld'):
        return {
            name.value: data.get_config_data(world) for name, data in self.rooms.items()
        }
