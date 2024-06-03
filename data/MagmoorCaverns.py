
from .RoomData import AreaData, PickupData, RoomData
from .RoomNames import RoomName


class MagmoorCavernsAreaData(AreaData):
    rooms = {
        RoomName.Burning_Trail: RoomData(doors={}, pickups=[]),
        RoomName.Fiery_Shores: RoomData(doors={}, pickups=[PickupData('Fiery Shores - Morph Track', required_items=[], tricks=[]), PickupData('Fiery Shores - Warrior Shrine Tunnel', required_items=[], tricks=[]), ]),
        RoomName.Geothermal_Core: RoomData(doors={}, pickups=[]),
        RoomName.Lake_Tunnel: RoomData(doors={}, pickups=[]),
        RoomName.Lava_Lake: RoomData(doors={}, pickups=[PickupData('Lava Lake', required_items=[], tricks=[]), ]),
        RoomName.Magmoor_Workstation: RoomData(doors={}, pickups=[PickupData('Magmoor Workstation', required_items=[], tricks=[]), ]),
        RoomName.Monitor_Station: RoomData(doors={}, pickups=[]),
        RoomName.Monitor_Tunnel: RoomData(doors={}, pickups=[]),
        RoomName.North_Core_Tunnel: RoomData(doors={}, pickups=[]),
        RoomName.Pit_Tunnel: RoomData(doors={}, pickups=[]),
        RoomName.Plasma_Processing: RoomData(doors={}, pickups=[PickupData('Plasma Processing', required_items=[], tricks=[]), ]),
        RoomName.Save_Station_Magmoor_A: RoomData(doors={}, pickups=[]),
        RoomName.Save_Station_Magmoor_B: RoomData(doors={}, pickups=[]),
        RoomName.Shore_Tunnel: RoomData(doors={}, pickups=[PickupData('Shore Tunnel', required_items=[], tricks=[]), ]),
        RoomName.South_Core_Tunnel: RoomData(doors={}, pickups=[]),
        RoomName.Storage_Cavern: RoomData(doors={}, pickups=[PickupData('Storage Cavern', required_items=[], tricks=[]), ]),
        RoomName.Transport_to_Chozo_Ruins_North: RoomData(doors={}, pickups=[]),
        RoomName.Transport_to_Phazon_Mines_West: RoomData(doors={}, pickups=[]),
        RoomName.Transport_to_Phendrana_Drifts_North: RoomData(doors={}, pickups=[]),
        RoomName.Transport_to_Phendrana_Drifts_South: RoomData(doors={}, pickups=[]),
        RoomName.Transport_to_Tallon_Overworld_West: RoomData(doors={}, pickups=[]),
        RoomName.Transport_Tunnel_A: RoomData(doors={}, pickups=[PickupData('Transport Tunnel A', required_items=[], tricks=[]), ]),
        RoomName.Transport_Tunnel_B: RoomData(doors={}, pickups=[]),
        RoomName.Transport_Tunnel_C: RoomData(doors={}, pickups=[]),
        RoomName.Triclops_Pit: RoomData(doors={}, pickups=[PickupData('Triclops Pit', required_items=[], tricks=[]), ]),
        RoomName.Twin_Fires_Tunnel: RoomData(doors={}, pickups=[]),
        RoomName.Twin_Fires: RoomData(doors={}, pickups=[]),
        RoomName.Warrior_Shrine: RoomData(doors={}, pickups=[PickupData('Warrior Shrine', required_items=[], tricks=[]), ]),
        RoomName.Workstation_Tunnel: RoomData(doors={}, pickups=[])
    }
