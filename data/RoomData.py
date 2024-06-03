from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from .RoomNames import RoomName
from .Tricks import Trick


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

@dataclass
class PickupData:
    name: str
    required_items: List[str]
    tricks: List[str]


@dataclass
class RoomData:
    doors: dict[int, DoorData]
    pickups: list[PickupData]


@dataclass
class AreaData:
    rooms: dict[RoomName, RoomData]
    # transports:
