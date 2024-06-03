
from .RoomData import AreaData, PickupData, RoomData
from .RoomNames import RoomName


class TallonOverworldAreaData(AreaData):
    rooms = {
        RoomName.Alcove: RoomData(doors={}, pickups=[PickupData('Alcove', required_items=[], tricks=[]), ]),
        RoomName.Arbor_Chamber: RoomData(doors={}, pickups=[PickupData('Arbor Chamber', required_items=[], tricks=[]), ]),
        RoomName.Artifact_Temple: RoomData(doors={}, pickups=[PickupData('Artifact Temple', required_items=[], tricks=[]), ]),
        RoomName.Biohazard_Containment: RoomData(doors={}, pickups=[PickupData('Biohazard Containment', required_items=[], tricks=[]), ]),
        RoomName.Biotech_Research_Area_1: RoomData(doors={}, pickups=[]),
        RoomName.Canyon_Cavern: RoomData(doors={}, pickups=[]),
        RoomName.Cargo_Freight_Lift_to_Deck_Gamma: RoomData(doors={}, pickups=[PickupData('Cargo Freight Lift to Deck Gamma', required_items=[], tricks=[]), ]),
        RoomName.Connection_Elevator_to_Deck_Beta: RoomData(doors={}, pickups=[]),
        RoomName.Deck_Beta_Conduit_Hall: RoomData(doors={}, pickups=[]),
        RoomName.Deck_Beta_Security_Hall: RoomData(doors={}, pickups=[]),
        RoomName.Deck_Beta_Transit_Hall: RoomData(doors={}, pickups=[]),
        RoomName.Frigate_Access_Tunnel: RoomData(doors={}, pickups=[]),
        RoomName.Frigate_Crash_Site: RoomData(doors={}, pickups=[PickupData('Frigate Crash Site', required_items=[], tricks=[]), ]),
        RoomName.Great_Tree_Chamber: RoomData(doors={}, pickups=[PickupData('Great Tree Chamber', required_items=[], tricks=[]), ]),
        RoomName.Great_Tree_Hall: RoomData(doors={}, pickups=[]),
        RoomName.Gully: RoomData(doors={}, pickups=[]),
        RoomName.Hydro_Access_Tunnel: RoomData(doors={}, pickups=[PickupData('Hydro Access Tunnel', required_items=[], tricks=[]), ]),
        RoomName.Landing_Site: RoomData(doors={}, pickups=[PickupData('Landing Site', required_items=[], tricks=[]), ]),
        RoomName.Life_Grove_Tunnel: RoomData(doors={}, pickups=[PickupData('Life Grove Tunnel', required_items=[], tricks=[]), ]),
        RoomName.Life_Grove: RoomData(doors={}, pickups=[PickupData('Life Grove - Start', required_items=[], tricks=[]), PickupData('Life Grove - Underwater Spinner', required_items=[], tricks=[]), ]),
        RoomName.Main_Ventilation_Shaft_Section_A: RoomData(doors={}, pickups=[]),
        RoomName.Main_Ventilation_Shaft_Section_B: RoomData(doors={}, pickups=[]),
        RoomName.Main_Ventilation_Shaft_Section_C: RoomData(doors={}, pickups=[]),
        RoomName.Overgrown_Cavern: RoomData(doors={}, pickups=[PickupData('Overgrown Cavern', required_items=[], tricks=[]), ]),
        RoomName.Reactor_Access: RoomData(doors={}, pickups=[]),
        RoomName.Reactor_Core: RoomData(doors={}, pickups=[]),
        RoomName.Root_Cave: RoomData(doors={}, pickups=[PickupData('Root Cave', required_items=[], tricks=[]), ]),
        RoomName.Root_Tunnel: RoomData(doors={}, pickups=[]),
        RoomName.Savestation: RoomData(doors={}, pickups=[]),
        RoomName.Tallon_Canyon: RoomData(doors={}, pickups=[]),
        RoomName.Temple_Hall: RoomData(doors={}, pickups=[]),
        RoomName.Temple_Lobby: RoomData(doors={}, pickups=[]),
        RoomName.Temple_Security_Station: RoomData(doors={}, pickups=[]),
        RoomName.Transport_to_Chozo_Ruins_East: RoomData(doors={}, pickups=[]),
        RoomName.Transport_to_Chozo_Ruins_South: RoomData(doors={}, pickups=[]),
        RoomName.Transport_to_Chozo_Ruins_West: RoomData(doors={}, pickups=[]),
        RoomName.Transport_to_Magmoor_Caverns_East: RoomData(doors={}, pickups=[]),
        RoomName.Transport_to_Phazon_Mines_East: RoomData(doors={}, pickups=[]),
        RoomName.Transport_Tunnel_A: RoomData(doors={}, pickups=[]),
        RoomName.Transport_Tunnel_B: RoomData(doors={}, pickups=[PickupData('Transport Tunnel B', required_items=[], tricks=[]), ]),
        RoomName.Transport_Tunnel_C: RoomData(doors={}, pickups=[]),
        RoomName.Transport_Tunnel_D: RoomData(doors={}, pickups=[]),
        RoomName.Transport_Tunnel_E: RoomData(doors={}, pickups=[]),
        RoomName.Waterfall_Cavern: RoomData(doors={}, pickups=[])
    }
