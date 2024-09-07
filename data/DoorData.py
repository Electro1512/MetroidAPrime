

from dataclasses import dataclass, field
from typing import Callable, List, Optional, TYPE_CHECKING
from .Tricks import TrickInfo
from BaseClasses import CollectionState
from .AreaNames import MetroidPrimeArea
from .RoomNames import RoomName
from ..DoorRando import DoorLockType
if TYPE_CHECKING:
    from .. import MetroidPrimeWorld
    from ..BlastShieldRando import BlastShieldType


@dataclass
class DoorData:
    default_destination: Optional[RoomName]
    defaultLock: DoorLockType = DoorLockType.Blue
    blast_shield: Optional['BlastShieldType'] = None
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


def get_door_data_by_room_names(source_room: RoomName, target_room: RoomName, area: MetroidPrimeArea, world: 'MetroidPrimeWorld') -> Optional[DoorData]:
    source_room_data = world.game_region_data.get(area).rooms.get(source_room)
    if not source_room_data:
        return None

    # Retrieve the target room data
    target_room_data = world.game_region_data.get(area).rooms.get(target_room)
    if not target_room_data:
        return None

    # Iterate through the doors in the source room to find a matching door
    for door_id, door_data in source_room_data.doors.items():
        if door_data.default_destination == target_room:
            return door_data, door_id

    return None
