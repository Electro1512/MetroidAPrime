
from worlds.metroidprime.LogicCombat import can_combat_mines, can_combat_omega_pirate
from worlds.metroidprime.data.Tricks import Tricks
from .RoomNames import RoomName
from worlds.metroidprime.data.AreaNames import MetroidPrimeArea
from .RoomData import AreaData, DoorData, DoorLockType, PickupData, RoomData
from worlds.metroidprime.Logic import can_backwards_lower_mines, can_bomb, can_boost, can_charge_beam, can_defeat_sheegoth, can_grapple, can_melt_ice, can_missile, can_morph_ball, can_move_underwater, can_phazon, can_plasma_beam, can_power_bomb, can_scan, can_space_jump, can_spider, can_super_missile, can_thermal, can_wave_beam, can_xray


class PhazonMinesAreaData(AreaData):
    rooms = {
        RoomName.Central_Dynamo: RoomData(
            area=MetroidPrimeArea.Phazon_Mines,
            doors={
                0: DoorData(RoomName.Dynamo_Access, rule_func=lambda state, player: can_combat_mines(state, player) and can_space_jump(state, player) and can_power_bomb(state, player), defaultLock=DoorLockType.Ice, destinationArea=MetroidPrimeArea.Phazon_Mines),
                1: DoorData(RoomName.Quarantine_Access_A, rule_func=lambda state, player: can_space_jump(state, player) and can_power_bomb(state, player), defaultLock=DoorLockType.Ice),
                2: DoorData(RoomName.Save_Station_Mines_B, defaultLock=DoorLockType.Ice),
            }, pickups=[PickupData('Phazon Mines: Central Dynamo', rule_func=can_bomb), ]),
        RoomName.Dynamo_Access: RoomData(
            area=MetroidPrimeArea.Phazon_Mines,
            doors={
                0: DoorData(RoomName.Central_Dynamo, defaultLock=DoorLockType.Ice, destinationArea=MetroidPrimeArea.Phazon_Mines),
                1: DoorData(RoomName.Omega_Research, defaultLock=DoorLockType.Ice),  # Vertical going up
            }),
        RoomName.Elevator_A: RoomData(doors={
            0: DoorData(RoomName.Elevator_Access_A, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Elite_Control_Access, defaultLock=DoorLockType.Ice, exclude_from_rando=True, rule_func=can_scan),  # Not annotated
        }),
        RoomName.Elevator_Access_A: RoomData(doors={
            0: DoorData(RoomName.Ore_Processing, defaultLock=DoorLockType.Ice, rule_func=can_spider, tricks=[Tricks.mines_climb_shafts_no_spider]),
            1: DoorData(RoomName.Elevator_A, defaultLock=DoorLockType.Ice,),
        }),
        RoomName.Elevator_Access_B: RoomData(doors={
            0: DoorData(RoomName.Metroid_Quarantine_B, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Elevator_B, defaultLock=DoorLockType.Plasma),
        }),
        RoomName.Elevator_B: RoomData(doors={
            0: DoorData(RoomName.Elevator_Access_B, defaultLock=DoorLockType.Plasma),
            1: DoorData(RoomName.Fungal_Hall_Access, defaultLock=DoorLockType.Plasma),
        }),
        RoomName.Elite_Control_Access: RoomData(doors={
            0: DoorData(RoomName.Elevator_A, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Elite_Control, defaultLock=DoorLockType.Wave),
        }, pickups=[PickupData('Phazon Mines: Elite Control Access', rule_func=can_morph_ball), ]),
        RoomName.Elite_Control: RoomData(doors={
            0: DoorData(RoomName.Maintenance_Tunnel, defaultLock=DoorLockType.Ice, rule_func=can_scan),
            1: DoorData(RoomName.Elite_Control_Access, defaultLock=DoorLockType.Wave, rule_func=can_scan),
            2: DoorData(RoomName.Ventilation_Shaft, defaultLock=DoorLockType.Ice, rule_func=can_scan),  # Vertical door going up
        }),
        RoomName.Elite_Quarters_Access: RoomData(doors={
            0: DoorData(RoomName.Metroid_Quarantine_B, defaultLock=DoorLockType.Plasma, rule_func=can_backwards_lower_mines),
            1: DoorData(RoomName.Elite_Quarters, defaultLock=DoorLockType.Plasma, rule_func=can_melt_ice),
        }),
        RoomName.Elite_Quarters: RoomData(
            doors={
                0: DoorData(RoomName.Elite_Quarters_Access, defaultLock=DoorLockType.Plasma, rule_func=lambda state, player: can_combat_omega_pirate(state, player) and can_xray(state, player, True)),
                1: DoorData(RoomName.Processing_Center_Access, defaultLock=DoorLockType.Plasma, rule_func=lambda state, player: can_combat_omega_pirate(state, player) and can_xray(state, player, True) and can_scan(state, player)),
            },
            pickups=[PickupData('Phazon Mines: Elite Quarters', rule_func=lambda state, player: can_combat_omega_pirate(state, player) and can_xray(state, player, True)), ]),
        RoomName.Elite_Research: RoomData(
            doors={
                0: DoorData(RoomName.Research_Access, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_bomb(state, player) and can_boost(state, player) and can_space_jump(state, player) and can_scan(state, player), tricks=[Tricks.elite_research_spinner_no_boost]),
                0: DoorData(RoomName.Security_Access_B, defaultLock=DoorLockType.Ice),  # Vertical door, going down
            },
            pickups=[PickupData('Phazon Mines: Elite Research - Phazon Elite', rule_func=can_power_bomb),
                     PickupData('Phazon Mines: Elite Research - Laser', rule_func=lambda state, player: can_bomb(state, player) and can_boost(state, player) and can_space_jump(state, player) and can_scan(state, player), tricks=[Tricks.elite_research_spinner_no_boost]), ]),
        RoomName.Fungal_Hall_A: RoomData(doors={
            0: DoorData(RoomName.Phazon_Mining_Tunnel, rule_func=can_space_jump, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Fungal_Hall_Access, rule_func=lambda state, player: can_grapple(state, player) and can_space_jump(state, player), defaultLock=DoorLockType.Ice, tricks=[Tricks.fungal_hall_a_no_grapple]),
        }),
        RoomName.Fungal_Hall_Access: RoomData(
            doors={
                0: DoorData(RoomName.Fungal_Hall_A, rule_func=lambda state, player: can_space_jump(state, player)),
                1: DoorData(RoomName.Elevator_B, rule_func=lambda state, player: can_space_jump(state, player)),
            },
            pickups=[PickupData('Phazon Mines: Fungal Hall Access', rule_func=lambda state, player: can_morph_ball(state, player) and can_phazon(state, player), tricks=[Tricks.fungal_hall_access_no_phazon_suit]), ]),
        RoomName.Fungal_Hall_B: RoomData(doors={
            0: DoorData(RoomName.Missile_Station_Mines, defaultLock=DoorLockType.Plasma, rule_func=lambda state, player: can_space_jump(state, player) and can_grapple(state, player),  tricks=[Tricks.fungal_hall_b_no_grapple]),
            1: DoorData(RoomName.Quarantine_Access_B, defaultLock=DoorLockType.Plasma, rule_func=lambda state, player: can_space_jump(state, player) and can_grapple(state, player),  tricks=[Tricks.fungal_hall_b_no_grapple]),
            2: DoorData(RoomName.Phazon_Mining_Tunnel, defaultLock=DoorLockType.Plasma, rule_func=can_space_jump, tricks=[Tricks.fungal_hall_b_no_grapple]),
        }, pickups=[PickupData('Phazon Mines: Fungal Hall B', rule_func=lambda state, player: can_bomb(state, player) or can_power_bomb(state, player)), ]),
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
        RoomName.Maintenance_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Elite_Control, rule_func=can_power_bomb, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Phazon_Processing_Center, rule_func=can_power_bomb, defaultLock=DoorLockType.Ice),
        }),
        RoomName.Map_Station_Mines: RoomData(doors={
            0: DoorData(RoomName.Omega_Research, rule_func=can_power_bomb, defaultLock=DoorLockType.Ice),
        }),
        RoomName.Metroid_Quarantine_A: RoomData(
            doors={
                0: DoorData(RoomName.Quarantine_Access_A, defaultLock=DoorLockType.Wave, rule_func=lambda state, player: can_combat_mines(state, player) and can_backwards_lower_mines(state, player) and can_space_jump(state, player)),
                1: DoorData(RoomName.Elevator_Access_B, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_combat_mines(state, player) and can_scan(state, player) and can_spider(state, player) and can_bomb(state, player) and can_space_jump(state, player) and can_xray(state, player), tricks=[Tricks.metroid_quarantine_a_no_spider])
            },
            pickups=[PickupData('Phazon Mines: Metroid Quarantine A', rule_func=lambda state, player: can_combat_mines(state, player) and (can_scan(state, player) or can_backwards_lower_mines(state, player)) and can_power_bomb(state, player) and can_space_jump(state, player) and can_xray(state, player), tricks=[]), ]),
        RoomName.Metroid_Quarantine_B: RoomData(
            doors={
                0: DoorData(RoomName.Quarantine_Access_B, defaultLock=DoorLockType.Plasma, rule_func=lambda state, player: can_combat_mines(state, player) and can_space_jump(state, player)),
                1: DoorData(RoomName.Elite_Quarters_Access, defaultLock=DoorLockType.Plasma, rule_func=lambda state, player: can_combat_mines(state, player) and can_spider(state, player) and can_grapple(state, player) and can_space_jump(state, player) and can_scan(state, player), tricks=[Tricks.metroid_quarantine_b_no_spider_grapple]),
                2: DoorData(RoomName.Save_Station_Mines_C, defaultLock=DoorLockType.Plasma, rule_func=lambda state, player: can_combat_mines(state, player) and can_spider(state, player) and can_grapple(state, player) and can_space_jump(state, player) and can_scan(state, player), tricks=[Tricks.metroid_quarantine_b_no_spider_grapple]),
            },
            pickups=[PickupData('Phazon Mines: Metroid Quarantine B', rule_func=lambda state, player: can_combat_mines(state, player) and state.can_reach(RoomName.Elite_Quarters_Access.value, None, player) and can_super_missile(state, player), tricks=[]), ]),
        RoomName.Mine_Security_Station: RoomData(doors={
            0: DoorData(RoomName.Security_Access_A, defaultLock=DoorLockType.Ice ),
            1: DoorData(RoomName.Security_Access_B, defaultLock=DoorLockType.Wave ),
            2: DoorData(RoomName.Storage_Depot_A, defaultLock=DoorLockType.Plasma, rule_func=lambda state, player: can_power_bomb(state, player) and can_plasma_beam(state, player) and can_scan(state, player)),
        }),
        RoomName.Missile_Station_Mines: RoomData(doors={
            0: DoorData(RoomName.Fungal_Hall_B, defaultLock=DoorLockType.Plasma),
        }),
        RoomName.Omega_Research: RoomData(doors={
            0: DoorData(RoomName.Map_Station_Mines, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_combat_mines(state, player) and can_power_bomb(state, player)),
            1: DoorData(RoomName.Ventilation_Shaft, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_combat_mines(state, player) and can_power_bomb(state, player)),
            2: DoorData(RoomName.Dynamo_Access, defaultLock=DoorLockType.Ice, destinationArea=MetroidPrimeArea.Phazon_Mines, rule_func=lambda state, player: can_combat_mines(state, player) and can_power_bomb(state, player)),  # Vertical door going down
        }),
        RoomName.Ore_Processing: RoomData(doors={
            0: DoorData(RoomName.Research_Access, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: True),
            1: DoorData(RoomName.Storage_Depot_B, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_spider(state, player) and can_bomb(state, player) and can_power_bomb(state, player), tricks=[Tricks.ore_processing_to_storage_depot_b_no_spider]),
            2: DoorData(RoomName.Waste_Disposal, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_spider(state, player) and can_grapple(state, player) and can_bomb(state, player) and can_power_bomb(state, player) and can_space_jump(state, player), tricks=[Tricks.ore_processing_climb_no_grapple_spider]),
            3: DoorData(RoomName.Elevator_Access_A, defaultLock=DoorLockType.Ice,  rule_func=lambda state, player: can_spider(state, player) and can_grapple(state, player) and can_bomb(state, player) and can_power_bomb(state, player) and can_space_jump(state, player), tricks=[Tricks.ore_processing_climb_no_grapple_spider]),
        }),
        RoomName.Phazon_Mining_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Fungal_Hall_B, rule_func=lambda state, player: can_bomb(state, player) and can_power_bomb(state, player), defaultLock=DoorLockType.Plasma),
            1: DoorData(RoomName.Fungal_Hall_A, rule_func=lambda state, player: can_bomb(state, player) and can_power_bomb(state, player), defaultLock=DoorLockType.Plasma),

        }, pickups=[PickupData('Phazon Mines: Phazon Mining Tunnel', rule_func=lambda state, player: can_phazon(state, player) and can_bomb(state, player), tricks=[]), ]),
        RoomName.Phazon_Processing_Center: RoomData(
            doors={
                0: DoorData(RoomName.Transport_Access, destinationArea=MetroidPrimeArea.Phazon_Mines, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_spider(state, player) and can_bomb(state, player) and can_space_jump(state, player), tricks=[Tricks.climb_phazon_processing_center_no_spider]),
                1: DoorData(RoomName.Maintenance_Tunnel, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_spider(state, player) and can_bomb(state, player) and can_space_jump(state, player), tricks=[Tricks.climb_phazon_processing_center_no_spider]),
                2: DoorData(RoomName.Processing_Center_Access, defaultLock=DoorLockType.Plasma),
            },
            pickups=[PickupData('Phazon Mines: Phazon Processing Center', rule_func=lambda state, player: can_spider(state, player) and can_bomb(state, player) and can_space_jump(state, player) and can_power_bomb(state, player), tricks=[Tricks.phazon_processing_center_item_no_spider]), ]),
        RoomName.Processing_Center_Access: RoomData(
            doors={
                0: DoorData(RoomName.Phazon_Processing_Center, rule_func=lambda state, player: can_scan(state, player) or can_backwards_lower_mines(state, player), defaultLock=DoorLockType.Plasma),
                1: DoorData(RoomName.Elite_Quarters, rule_func=lambda state, player: can_backwards_lower_mines(state, player), defaultLock=DoorLockType.Plasma),
            },
            pickups=[PickupData('Phazon Mines: Processing Center Access', rule_func=lambda state, player: can_backwards_lower_mines(state, player) or state.can_reach(RoomName.Elite_Quarters.value, None, player), tricks=[]), ]),
        RoomName.Quarantine_Access_A: RoomData(doors={
            0: DoorData(RoomName.Central_Dynamo, defaultLock=DoorLockType.Ice, destinationArea=MetroidPrimeArea.Phazon_Mines),
            1: DoorData(RoomName.Metroid_Quarantine_A, defaultLock=DoorLockType.Wave),
        }),
        RoomName.Quarantine_Access_B: RoomData(doors={
            0: DoorData(RoomName.Metroid_Quarantine_B, defaultLock=DoorLockType.Plasma),
            1: DoorData(RoomName.Fungal_Hall_B, defaultLock=DoorLockType.Plasma),
        }),
        RoomName.Quarry_Access: RoomData(doors={
            0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Wave),
            1: DoorData(RoomName.Transport_to_Tallon_Overworld_South, defaultLock=DoorLockType.Wave, destinationArea=MetroidPrimeArea.Phazon_Mines),
        }),
        RoomName.Research_Access: RoomData(doors={
            0: DoorData(RoomName.Ore_Processing, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Elite_Research, defaultLock=DoorLockType.Ice, rule_func=can_spider, tricks=[Tricks.mines_climb_shafts_no_spider]),
        }),
        RoomName.Save_Station_Mines_A: RoomData(doors={
            0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Wave),
        }),
        RoomName.Save_Station_Mines_B: RoomData(doors={
            0: DoorData(RoomName.Central_Dynamo, defaultLock=DoorLockType.Ice, destinationArea=MetroidPrimeArea.Phazon_Mines),
        }),
        RoomName.Save_Station_Mines_C: RoomData(doors={
            0: DoorData(RoomName.Metroid_Quarantine_B, defaultLock=DoorLockType.Plasma),
        }),
        RoomName.Security_Access_A: RoomData(doors={
            0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Mine_Security_Station, defaultLock=DoorLockType.Ice),
        }, pickups=[PickupData('Phazon Mines: Security Access A', rule_func=can_power_bomb, tricks=[]), ]),
        RoomName.Security_Access_B: RoomData(doors={
            0: DoorData(RoomName.Mine_Security_Station, defaultLock=DoorLockType.Wave),  # Vertical door going down
            1: DoorData(RoomName.Elite_Research, defaultLock=DoorLockType.Ice),  # Vertical door going up
        }),
        RoomName.Storage_Depot_A: RoomData(doors={0: DoorData(RoomName.Mine_Security_Station, defaultLock=DoorLockType.Plasma), }, pickups=[PickupData('Phazon Mines: Storage Depot A'), ]),
        RoomName.Storage_Depot_B: RoomData(doors={0: DoorData(RoomName.Ore_Processing, defaultLock=DoorLockType.Ice), }, pickups=[PickupData('Phazon Mines: Storage Depot B'), ]),
        RoomName.Transport_Access: RoomData(area=MetroidPrimeArea.Phazon_Mines, doors={
            0: DoorData(RoomName.Phazon_Processing_Center, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Transport_to_Magmoor_Caverns_South, defaultLock=DoorLockType.Ice, destinationArea=MetroidPrimeArea.Phazon_Mines),
        }),
        RoomName.Transport_to_Magmoor_Caverns_South: RoomData(
            area=MetroidPrimeArea.Phazon_Mines,
            doors={
                0: DoorData(RoomName.Transport_Access, defaultLock=DoorLockType.Ice, destinationArea=MetroidPrimeArea.Phazon_Mines),
            }),
        RoomName.Transport_to_Tallon_Overworld_South: RoomData(
            area=MetroidPrimeArea.Phazon_Mines,
            doors={
                0: DoorData(RoomName.Quarry_Access, defaultLock=DoorLockType.Wave,),
            }),
        RoomName.Ventilation_Shaft: RoomData(
            doors={
                0: DoorData(RoomName.Omega_Research, defaultLock=DoorLockType.Ice),
                1: DoorData(RoomName.Elite_Control, defaultLock=DoorLockType.Ice, rule_func=can_boost, tricks=[Tricks.ventilation_shaft_hpbj]),
            },
            pickups=[PickupData('Phazon Mines: Ventilation Shaft', rule_func=lambda state, player: can_scan(state, player) and can_power_bomb(state, player) and can_space_jump(state, player)), ]),
        RoomName.Waste_Disposal: RoomData(doors={
            0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Ice, rule_func=can_bomb),
            1: DoorData(RoomName.Ore_Processing, defaultLock=DoorLockType.Ice, rule_func=can_bomb),

        })
    }
