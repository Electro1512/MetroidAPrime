
from .RoomData import AreaData, PickupData, RoomData
from .RoomNames import RoomName


class EndCinemaAreaData(AreaData):
    rooms = {
        RoomName.End_Cinema: RoomData(doors={}, pickups=[])
    }
