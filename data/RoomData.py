from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import typing

from ..Locations import METROID_PRIME_LOCATION_BASE, every_location
from .RoomNames import RoomName
from .Tricks import Trick, TrickDifficulty

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


class DoorLockType(Enum):
    Blue = "Blue"
    Wave_Beam = "Wave Beam"
    Ice_Beam = "Ice Beam"
    Plasma_Beam = "Plasma Beam"
    Missile = "Missile"


@dataclass
class DoorData:
    index: int
    defaultLock: DoorLockType
    lock: DoorLockType
    destination: Optional[RoomName]
    required_items: List[str]


@dataclass
class TrickData:
    name: Trick
    required_items: List[str]
    difficulty: TrickDifficulty


@dataclass
class PickupData:
    name: str
    required_items: List[str]
    tricks: List[TrickData]

    def get_config_data(self, world: 'MetroidPrimeWorld'):
        return {
            "type": "Unknown Item 1",
            "scanText": get_config_item_text(world, self.name),
            "hudmemoText": get_config_item_text(world, self.name) + " Acquired!",
            "currIncrease": every_location[self.name] - METROID_PRIME_LOCATION_BASE + 1,
            "model": get_config_item_model(world, self.name),
            "showIcon": True
        }


@dataclass
class RoomData:
    doors: dict[int, DoorData]
    pickups: list[PickupData]

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
