
from .RoomData import AreaData, PickupData, RoomData
from .RoomNames import RoomName


class ImpactCraterAreaData(AreaData):
    rooms = {
        RoomName.Crater_Entry_Point: RoomData(doors={}, pickups=[])
    }
