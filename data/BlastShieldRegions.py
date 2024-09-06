from dataclasses import dataclass
from typing import Dict, List

from .RoomNames import RoomName

from .AreaNames import MetroidPrimeArea


@dataclass
class BlastShieldRegion:
    doors: Dict[RoomName, RoomName]
    can_be_locked: bool = False


@dataclass
class BlastShieldArea:
    """Regions used to determine where blast shields can be placed within a prime area"""
    area: MetroidPrimeArea
    regions: List[BlastShieldRegion]


ChozoRuinsBlastShieldRegions = BlastShieldArea(
    area=MetroidPrimeArea.Chozo_Ruins,
    regions=[
        BlastShieldRegion(
            doors={
                RoomName.Transport_to_Tallon_Overworld_North: RoomName.Ruins_Entrance,
                RoomName.Ruins_Entrance: RoomName.Main_Plaza
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Transport_to_Tallon_Overworld_North: RoomName.Ruins_Entrance,
                RoomName.Ruins_Entrance: RoomName.Main_Plaza
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Main_Plaza: RoomName.Ruined_Shrine_Access,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Ruined_Shrine: RoomName.Tower_of_Light_Access,
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Main_Plaza: RoomName.Nursery_Access,
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.North_Atrium: RoomName.Ruined_Gallery,
                RoomName.Totem_Access: RoomName.Hive_Totem,
                RoomName.Transport_Access_North: RoomName.Transport_to_Magmoor_Caverns_North
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Transport_to_Magmoor_Caverns_North: RoomName.Vault_Access,
                RoomName.Vault: RoomName.Plaza_Access,
                RoomName.Plaza_Access: RoomName.Main_Plaza,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Main_Plaza: RoomName.Ruined_Fountain_Access,
                RoomName.Ruined_Fountain: RoomName.Meditation_Fountain,
                RoomName.Meditation_Fountain: RoomName.Magma_Pool,
                RoomName.Magma_Pool: RoomName.Training_Chamber_Access,
                RoomName.Training_Chamber_Access: RoomName.Training_Chamber,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Ruined_Fountain: RoomName.Arboretum_Access,
                RoomName.Arboretum_Access: RoomName.Arboretum,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Arboretum: RoomName.Sunchamber_Lobby,
                RoomName.Arboretum: RoomName.Gathering_Hall_Access,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Gathering_Hall: RoomName.Watery_Hall_Access,
                RoomName.Watery_Hall: RoomName.Dynamo_Access
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Gathering_Hall: RoomName.East_Atrium,
                RoomName.Energy_Core_Access: RoomName.Energy_Core,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Energy_Core: RoomName.Burn_Dome_Access,
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Furnace: RoomName.East_Furnace_Access
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Crossway_Access_West: RoomName.Crossway,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Crossway: RoomName.Elder_Hall_Access,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Hall_of_the_Elders: RoomName.Reflecting_Pool_Access
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Reflecting_Pool: RoomName.Antechamber,
                RoomName.Reflecting_Pool: RoomName.Save_Station_3,
                RoomName.Reflecting_Pool: RoomName.Transport_Access_South
            }
        ),

    ]
)

TallonOverworldBlastShieldRegions = BlastShieldArea(
    area=MetroidPrimeArea.Tallon_Overworld,
    regions=[
        BlastShieldRegion(
            doors={
                RoomName.Landing_Site: RoomName.Alcove,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Landing_Site: RoomName.Canyon_Cavern
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Landing_Site: RoomName.Temple_Hall
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Landing_Site: RoomName.Waterfall_Cavern
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Tallon_Canyon: RoomName.Root_Tunnel,
                RoomName.Root_Cave: RoomName.Transport_Tunnel_B,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Great_Tree_Hall: RoomName.Transport_Tunnel_D,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Great_Tree_Hall: RoomName.Transport_Tunnel_E,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Great_Tree_Hall: RoomName.Great_Tree_Chamber
            }
        ),
    ]
)

PhendranaDriftsBlastShieldRegions = BlastShieldArea(
    area=MetroidPrimeArea.Phendrana_Drifts,
    regions=[
        BlastShieldRegion(
            doors={
                RoomName.Phendrana_Shorelines: RoomName.Shoreline_Entrance
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Phendrana_Shorelines: RoomName.Temple_Entryway
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Phendrana_Shorelines: RoomName.Ice_Ruins_Access,
                RoomName.Phendrana_Shorelines: RoomName.Plaza_Walkway
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Phendrana_Shorelines: RoomName.Ruins_Entryway,
                RoomName.Ruins_Entryway: RoomName.Ice_Ruins_West
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Ice_Ruins_West: RoomName.Canyon_Entryway
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Ice_Ruins_West: RoomName.Courtyard_Entryway
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Ruined_Courtyard: RoomName.Quarantine_Access
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Ruined_Courtyard: RoomName.Specimen_Storage
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Quarantine_Cave: RoomName.South_Quarantine_Tunnel
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Research_Lab_Hydra: RoomName.Observatory_Access,
                RoomName.Observatory: RoomName.West_Tower_Entrance,
                RoomName.Control_Tower: RoomName.East_Tower,
                RoomName.Research_Lab_Aether: RoomName.Research_Core_Access,
                RoomName.Research_Core: RoomName.Pike_Access
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Transport_to_Magmoor_Caverns_South: RoomName.Transport_Access,
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Frozen_Pike: RoomName.Frost_Cave_Access,
                RoomName.Frost_Cave: RoomName.Upper_Edge_Tunnel,
                RoomName.Hunter_Cave: RoomName.Lower_Edge_Tunnel
            }
        ),

    ]
)

MagmoorCavernsBlastShieldRegions = BlastShieldArea(
    area=MetroidPrimeArea.Magmoor_Caverns,
    regions=[
        BlastShieldRegion(
            doors={
                RoomName.Transport_to_Chozo_Ruins_North: RoomName.Burning_Trail,
                RoomName.Lake_Tunnel: RoomName.Lava_Lake,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Lava_Lake: RoomName.Pit_Tunnel
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Triclops_Pit: RoomName.Storage_Cavern
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Monitor_Station: RoomName.Transport_Tunnel_A,
                RoomName.Transport_to_Phendrana_Drifts_North: RoomName.Transport_Tunnel_A
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Monitor_Station: RoomName.Warrior_Shrine
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Fiery_Shores: RoomName.Transport_Tunnel_B
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Transport_to_Tallon_Overworld_West: RoomName.Twin_Fires_Tunnel,
                RoomName.Twin_Fires_Tunnel: RoomName.Twin_Fires,
                RoomName.North_Core_Tunnel: RoomName.Geothermal_Core
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.South_Core_Tunnel: RoomName.Magmoor_Workstation,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Magmoor_Workstation: RoomName.Transport_Tunnel_C
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Magmoor_Workstation: RoomName.Workstation_Tunnel
            }
        ),

    ]
)

PhazonMinesBlastShieldRegions = BlastShieldArea(
    area=MetroidPrimeArea.Phazon_Mines,
    regions=[
        BlastShieldRegion(
            doors={
                RoomName.Main_Quarry: RoomName.Quarry_Access,
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Main_Quarry: RoomName.Waste_Disposal
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Main_Quarry: RoomName.Security_Access_A,
                RoomName.Security_Access_B: RoomName.Elite_Research,
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Research_Access: RoomName.Ore_Processing
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Ore_Processing: RoomName.Elevator_Access_A,
                RoomName.Elevator_Access_A: RoomName.Elevator_A
            }
        ),
        BlastShieldRegion(
            doors={
                RoomName.Ore_Processing: RoomName.Storage_Depot_B
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Elite_Control_Access: RoomName.Elite_Control
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Elite_Control: RoomName.Maintenance_Tunnel
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Elite_Control: RoomName.Ventilation_Shaft
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Central_Dynamo: RoomName.Quarantine_Access_A,
                RoomName.Metroid_Quarantine_A: RoomName.Quarantine_Access_A,
                RoomName.Metroid_Quarantine_A: RoomName.Elevator_Access_B
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Fungal_Hall_Access: RoomName.Fungal_Hall_A,
                RoomName.Fungal_Hall_A: RoomName.Phazon_Mining_Tunnel,
                RoomName.Fungal_Hall_B: RoomName.Quarantine_Access_B,
                RoomName.Metroid_Quarantine_B: RoomName.Elite_Quarters_Access
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Elite_Quarters: RoomName.Processing_Center_Access
            }
        ),
        BlastShieldRegion(
            can_be_locked=True,
            doors={
                RoomName.Phazon_Processing_Center: RoomName.Maintenance_Tunnel
            }
        ),
    ]
)


def get_blast_shield_regions_by_area(area: MetroidPrimeArea) -> BlastShieldArea:
    if area == MetroidPrimeArea.Chozo_Ruins:
        return ChozoRuinsBlastShieldRegions
    elif area == MetroidPrimeArea.Tallon_Overworld:
        return TallonOverworldBlastShieldRegions
    elif area == MetroidPrimeArea.Phendrana_Drifts:
        return PhendranaDriftsBlastShieldRegions
    elif area == MetroidPrimeArea.Magmoor_Caverns:
        return MagmoorCavernsBlastShieldRegions
    elif area == MetroidPrimeArea.Phazon_Mines:
        return PhazonMinesBlastShieldRegions
