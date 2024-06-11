
from worlds.metroidprime.data.Tricks import Tricks
from .RoomNames import RoomName
from .RoomData import AreaData, DoorData, DoorLockType, MetroidPrimeArea, PickupData, RoomData
from worlds.metroidprime.Logic2 import can_bomb, can_boost, can_charge_beam, can_defeat_sheegoth, can_grapple, can_melt_ice, can_missile, can_morph_ball, can_move_underwater, can_plasma_beam, can_power_bomb, can_scan, can_space_jump, can_spider, can_super_missile, can_thermal, can_wave_beam, can_xray


class PhazonMinesAreaData(AreaData):
    rooms = {
        RoomName.Central_Dynamo: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Central Dynamo', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Dynamo_Access: RoomData(doors={}),
        RoomName.Elevator_A: RoomData(doors={
            0: DoorData(RoomName.Elevator_Access_A, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Elite_Control_Access, defaultLock=DoorLockType.Ice, exclude_from_rando=True, rule_func=can_scan),  # Not annotated
        }),
        RoomName.Elevator_Access_A: RoomData(doors={
            0: DoorData(RoomName.Ore_Processing, defaultLock=DoorLockType.Ice, rule_func=can_spider, tricks=[Tricks.mines_climb_shafts_no_spider]),
            1: DoorData(RoomName.Elevator_A, defaultLock=DoorLockType.Ice,),
        }),
        RoomName.Elevator_Access_B: RoomData(doors={}),
        RoomName.Elevator_B: RoomData(doors={}),
        RoomName.Elite_Control_Access: RoomData(doors={

          }, pickups=[PickupData('Phazon Mines: Elite Control Access', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Elite_Control: RoomData(doors={}),
        RoomName.Elite_Quarters_Access: RoomData(doors={}),
        RoomName.Elite_Quarters: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Elite Quarters', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Elite_Research: RoomData(
            doors={
                0: DoorData(RoomName.Research_Access, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_bomb(state, player) and can_boost(state, player) and can_space_jump(state, player) and can_scan(state, player), tricks=[Tricks.elite_research_spinner_no_boost]),
                0: DoorData(RoomName.Security_Access_B, defaultLock=DoorLockType.Ice),  # Vertical door, going down
            },
            pickups=[PickupData('Phazon Mines: Elite Research - Phazon Elite', rule_func=can_power_bomb),
                     PickupData('Phazon Mines: Elite Research - Laser', rule_func=lambda state, player: can_bomb(state, player) and can_boost(state, player) and can_space_jump(state, player) and can_scan(state, player), tricks=[Tricks.elite_research_spinner_no_boost]), ]),
        RoomName.Fungal_Hall_A: RoomData(doors={}),
        RoomName.Fungal_Hall_Access: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Fungal Hall Access', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Fungal_Hall_B: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Fungal Hall B', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Main_Quarry: RoomData(
            doors={
                0: DoorData(RoomName.Waste_Disposal, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_grapple(state, player) and can_space_jump(state, player), tricks=[Tricks.main_quarry_to_waste_disposal_no_grapple]),
                1: DoorData(RoomName.Quarry_Access, defaultLock=DoorLockType.Wave,),
                2: DoorData(RoomName.Save_Station_Mines_A, defaultLock=DoorLockType.Wave, rule_func=can_spider),
                3: DoorData(RoomName.Security_Access_A, defaultLock=DoorLockType.Ice, rule_func=can_scan),
            },
            pickups=[PickupData('Phazon Mines: Main Quarry',
                                rule_func=lambda state, player: can_morph_ball(state, player) and can_spider(state, player) and can_bomb(state, player) and can_thermal(state, player) and can_wave_beam(state, player) and can_scan(state, player) and can_space_jump(state, player),
                                tricks=[Tricks.main_quarry_item_no_spider]),
                     ]),
        RoomName.Maintenance_Tunnel: RoomData(doors={}),
        RoomName.Map_Station_Mines: RoomData(doors={}),
        RoomName.Metroid_Quarantine_A: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Metroid Quarantine A', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Metroid_Quarantine_B: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Metroid Quarantine B', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Mine_Security_Station: RoomData(doors={
            0: DoorData(RoomName.Security_Access_A, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Security_Access_B, defaultLock=DoorLockType.Wave),
            2: DoorData(RoomName.Storage_Depot_A, defaultLock=DoorLockType.Plasma, rule_func=lambda state, player: can_power_bomb(state, player) and can_plasma_beam(state, player) and can_scan(state, player)),
        }),
        RoomName.Missile_Station_Mines: RoomData(doors={}),
        RoomName.Omega_Research: RoomData(doors={}),
        RoomName.Ore_Processing: RoomData(doors={
            0: DoorData(RoomName.Research_Access, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: True),
            1: DoorData(RoomName.Storage_Depot_B, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_spider(state, player) and can_bomb(state, player) and can_power_bomb(state, player), tricks=[Tricks.ore_processing_to_storage_depot_b_no_spider]),
            2: DoorData(RoomName.Waste_Disposal, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_spider(state, player) and can_grapple(state, player) and can_bomb(state, player) and can_power_bomb(state, player) and can_space_jump(state, player), tricks=[Tricks.ore_processing_climb_no_grapple_spider]),
            3: DoorData(RoomName.Elevator_Access_A, defaultLock=DoorLockType.Ice,  rule_func=lambda state, player: can_spider(state, player) and can_grapple(state, player) and can_bomb(state, player) and can_power_bomb(state, player) and can_space_jump(state, player), tricks=[Tricks.ore_processing_climb_no_grapple_spider]),
        }),
        RoomName.Phazon_Mining_Tunnel: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Phazon Mining Tunnel', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Phazon_Processing_Center: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Phazon Processing Center', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Processing_Center_Access: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Processing Center Access', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Quarantine_Access_A: RoomData(doors={}),
        RoomName.Quarantine_Access_B: RoomData(doors={}),
        RoomName.Quarry_Access: RoomData(doors={
            0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Wave),
        }),
        RoomName.Research_Access: RoomData(doors={
            0: DoorData(RoomName.Ore_Processing, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Elite_Research, defaultLock=DoorLockType.Ice, rule_func=can_spider, tricks=[Tricks.mines_climb_shafts_no_spider]),
        }),
        RoomName.Save_Station_Mines_A: RoomData(doors={}),
        RoomName.Save_Station_Mines_B: RoomData(doors={}),
        RoomName.Save_Station_Mines_C: RoomData(doors={}),
        RoomName.Security_Access_A: RoomData(doors={
            0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Mine_Security_Station, defaultLock=DoorLockType.Ice),
        }, pickups=[PickupData('Phazon Mines: Security Access A', rule_func=can_power_bomb, tricks=[]), ]),
        RoomName.Security_Access_B: RoomData(doors={
            0: DoorData(RoomName.Mine_Security_Station, defaultLock=DoorLockType.Wave),  # Vertical door going down
            1: DoorData(RoomName.Elite_Research, defaultLock=DoorLockType.Ice),  # Vertical door going up
        }),
        RoomName.Storage_Depot_A: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Storage Depot A', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Storage_Depot_B: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Storage Depot B', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Transport_Access: RoomData(doors={}),
        RoomName.Transport_to_Magmoor_Caverns_South: RoomData(doors={}),
        RoomName.Transport_to_Tallon_Overworld_South: RoomData(doors={
            0: DoorData(RoomName.Quarry_Access, defaultLock=DoorLockType.Wave),
        }),
        RoomName.Ventilation_Shaft: RoomData(doors={}, pickups=[PickupData('Phazon Mines: Ventilation Shaft', rule_func=lambda state, player: False, tricks=[]), ]),
        RoomName.Waste_Disposal: RoomData(doors={
            0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Ice, rule_func=can_bomb),
            1: DoorData(RoomName.Ore_Processing, defaultLock=DoorLockType.Ice, rule_func=can_bomb),

        })
    }
