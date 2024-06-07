from BaseClasses import LocationProgressType
from worlds.metroidprime.Items import SuitUpgrade
from .RoomData import AreaData, DoorData, DoorLockType, MetroidPrimeArea, PickupData, RoomData
from worlds.metroidprime.Logic2 import can_bomb, can_boost, can_climb_sun_tower, can_climb_tower_of_light, can_exit_ruined_shrine, can_flaahgra, can_grapple, can_heat, can_ice_beam, can_missile, can_morph_ball, can_move_underwater, can_plasma_beam, can_power_bomb, can_scan, can_space_jump, can_spider, can_super_missile, can_wave_beam
from worlds.metroidprime.data.Tricks import Tricks
from .RoomNames import RoomName


class ChozoRuinsAreaData(AreaData):
    rooms = {
        RoomName.Antechamber: RoomData(doors={0: DoorData(RoomName.Reflecting_Pool, defaultLock=DoorLockType.Ice)}, pickups=[PickupData('Chozo Ruins: Antechamber'), ]),
        RoomName.Arboretum_Access: RoomData(doors={
            0: DoorData(RoomName.Arboretum),
            1: DoorData(RoomName.Ruined_Fountain),
        }),
        RoomName.Arboretum: RoomData(doors={
            0: DoorData(RoomName.Sunchamber_Lobby, rule_func=lambda state, player: can_bomb(state, player) and can_scan(state, player), defaultLock=DoorLockType.Missile, tricks=[Tricks.arboretum_scan_gate_skip]),
            1: DoorData(RoomName.Arboretum_Access, defaultLock=DoorLockType.Missile),
            2: DoorData(RoomName.Gathering_Hall_Access, defaultLock=DoorLockType.Missile),
        }),
        RoomName.Burn_Dome_Access: RoomData(doors={
            0: DoorData(RoomName.Burn_Dome),
            1: DoorData(RoomName.Energy_Core, rule_func=can_bomb, defaultLock=DoorLockType.None_, exclude_from_rando=True),
        }),
        RoomName.Burn_Dome: RoomData(doors={}, pickups=[PickupData('Chozo Ruins: Burn Dome - Missile', rule_func=can_bomb), PickupData('Chozo Ruins: Burn Dome - Incinerator Drone'), ]),
        RoomName.Crossway_Access_South: RoomData(doors={
            0: DoorData(RoomName.Crossway, defaultLock=DoorLockType.Ice, rule_func=can_morph_ball),
            1: DoorData(RoomName.Hall_of_the_Elders, defaultLock=DoorLockType.Ice, rule_func=can_morph_ball),
        }),
        RoomName.Crossway_Access_West: RoomData(doors={
            0: DoorData(RoomName.Crossway, defaultLock=DoorLockType.Wave, rule_func=can_morph_ball),
            1: DoorData(RoomName.Furnace, rule_func=can_morph_ball, exclude_from_rando=True),
        }, pickups=[]),
        RoomName.Crossway: RoomData(
            doors={
                0: DoorData(RoomName.Crossway_Access_South, defaultLock=DoorLockType.Ice),
                1: DoorData(RoomName.Crossway_Access_West),
                2: DoorData(RoomName.Elder_Hall_Access, defaultLock=DoorLockType.Missile, rule_func=lambda state, player: can_boost(state, player), tricks=[Tricks.crossway_hpbj]),
            },
            pickups=[PickupData('Chozo Ruins: Crossway', rule_func=lambda state, player: can_bomb(state, player) and can_boost(state, player) and can_spider(state, player) and can_super_missile(state, player) and can_scan(state, player), tricks=[Tricks.crossway_item_fewer_reqs]), ]),
        RoomName.Dynamo_Access: RoomData(
            area=MetroidPrimeArea.Chozo_Ruins,
            doors={
                0: DoorData(RoomName.Watery_Hall, defaultLock=DoorLockType.Missile),
                1: DoorData(RoomName.Dynamo, destinationArea=MetroidPrimeArea.Chozo_Ruins),
            }),
        RoomName.Dynamo: RoomData(
            area=MetroidPrimeArea.Chozo_Ruins,
            doors={
                0: DoorData(RoomName.Dynamo_Access, destinationArea=MetroidPrimeArea.Chozo_Ruins),
            },
            pickups=[PickupData('Chozo Ruins: Dynamo - Lower', rule_func=can_super_missile), PickupData('Chozo Ruins: Dynamo - Spider Track', rule_func=can_spider), ]),
        RoomName.East_Atrium: RoomData(doors={
            0: DoorData(RoomName.Gathering_Hall),
            1: DoorData(RoomName.Energy_Core_Access),
        }),
        RoomName.East_Furnace_Access: RoomData(doors={
            0: DoorData(RoomName.Hall_of_the_Elders, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Furnace, defaultLock=DoorLockType.Ice)
        }),
        RoomName.Elder_Chamber: RoomData(
            doors={
                0: DoorData(RoomName.Hall_of_the_Elders, defaultLock=DoorLockType.Ice),
            },
            pickups=[PickupData('Chozo Ruins: Elder Chamber')]),
        RoomName.Elder_Hall_Access: RoomData(doors={
            0: DoorData(RoomName.Hall_of_the_Elders),
            1: DoorData(RoomName.Crossway, defaultLock=DoorLockType.Missile),
        }),
        RoomName.Energy_Core_Access: RoomData(doors={
            0: DoorData(RoomName.Energy_Core),
            1: DoorData(RoomName.East_Atrium),
        }),
        RoomName.Energy_Core: RoomData(doors={
            0: DoorData(RoomName.Burn_Dome_Access, defaultLock=DoorLockType.None_, rule_func=can_bomb, exclude_from_rando=True),  # Bombs are required to get out of here
            1: DoorData(RoomName.West_Furnace_Access, rule_func=can_bomb),
            2: DoorData(RoomName.Energy_Core_Access),
        }),
        RoomName.Eyon_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Ruined_Nursery),
            1: DoorData(RoomName.Nursery_Access),
        }),
        RoomName.Furnace: RoomData(
            doors={
                0: DoorData(RoomName.East_Furnace_Access, defaultLock=DoorLockType.Ice, rule_func=can_space_jump),
                1: DoorData(RoomName.West_Furnace_Access, rule_func=can_bomb),
                2: DoorData(RoomName.Crossway_Access_West, exclude_from_rando=True, rule_func=can_morph_ball, defaultLock=DoorLockType.None_),
            },
            pickups=[
                PickupData('Chozo Ruins: Furnace - Spider Tracks', rule_func=lambda state, player: can_power_bomb(state, player) and can_boost(state, player) and can_spider(state, player),
                           tricks=[Tricks.furnace_spider_track_hbj, Tricks.furnace_spider_track_sj_bombs]),
            ]),
        RoomName.Gathering_Hall_Access: RoomData(doors={
            0: DoorData(RoomName.Gathering_Hall),
            1: DoorData(RoomName.Arboretum, defaultLock=DoorLockType.Missile),
        }),
        RoomName.Gathering_Hall: RoomData(doors={
            0: DoorData(RoomName.Watery_Hall_Access),
            1: DoorData(RoomName.Gathering_Hall_Access, defaultLock=DoorLockType.Missile),
            2: DoorData(RoomName.Save_Station_2, defaultLock=DoorLockType.Missile),
            3: DoorData(RoomName.East_Atrium, rule_func=lambda state, player: can_morph_ball(state, player) or can_space_jump(state, player)),
        }, pickups=[PickupData('Chozo Ruins: Gathering Hall', rule_func=lambda state, player: can_space_jump(state, player) and can_power_bomb(state, player), tricks=[Tricks.gathering_hall_without_space_jump]), ]),
        RoomName.Hall_of_the_Elders: RoomData(
            doors={
                0: DoorData(RoomName.Reflecting_Pool_Access, rule_func=lambda state, player: can_bomb(state, player) and can_spider(state, player) and can_wave_beam(state, player), tricks=[Tricks.hall_of_elders_reflecting_pool_no_spider, Tricks.hall_of_elders_reflecting_pool_no_wave_beam]),
                1: DoorData(RoomName.Elder_Hall_Access, rule_func=lambda state, player: can_boost(state, player) and can_missile(state, player)),
                2: DoorData(RoomName.East_Furnace_Access, defaultLock=DoorLockType.Ice),
                3: DoorData(RoomName.Crossway_Access_South, defaultLock=DoorLockType.Ice),
                4: DoorData(RoomName.Elder_Chamber, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_bomb(state, player) and can_plasma_beam(state, player) and can_space_jump(state, player) and can_spider(state, player), tricks=[Tricks.hall_of_elders_elder_chamber_no_spider]),
            },
            pickups=[PickupData('Chozo Ruins: Hall of the Elders', rule_func=lambda state, player: can_bomb(state, player) and can_spider(state, player) and can_ice_beam(state, player) and can_space_jump(state, player), tricks=[Tricks.hall_of_elders_item_no_spider]), ]),
        RoomName.Hive_Totem: RoomData(
            doors={
                0: DoorData(RoomName.Totem_Access),
                1: DoorData(RoomName.Transport_Access_North, defaultLock=DoorLockType.Missile),
            },
            pickups=[PickupData('Chozo Ruins: Hive Totem'), ]),
        RoomName.Magma_Pool: RoomData(
            doors={
                0: DoorData(RoomName.Training_Chamber_Access, defaultLock=DoorLockType.Wave, rule_func=lambda state, player: can_grapple(state, player) and can_heat(state, player), tricks=[Tricks.magma_pool_scan_dash]),
                1: DoorData(RoomName.Meditation_Fountain, rule_func=lambda state, player: state.has(SuitUpgrade.Energy_Tank, player, 2) or state.has(SuitUpgrade.Varia_Suit, player) or state.has(SuitUpgrade.Gravity_Suit, player) or state.has(SuitUpgrade.Phazon_Suit, player)),  # Damage reduction let's player cross
            },
            pickups=[PickupData('Chozo Ruins: Magma Pool', rule_func=lambda state, player:  can_grapple(state, player) and can_heat(state, player) and can_power_bomb(state, player), tricks=[Tricks.magma_pool_item_infinite_speed, Tricks.magma_pool_item_scan_dash]), ]),
        RoomName.Main_Plaza: RoomData(doors={
            0: DoorData(RoomName.Ruined_Fountain_Access),
            1: DoorData(RoomName.Ruins_Entrance),
            2: DoorData(RoomName.Ruined_Shrine_Access, defaultLock=DoorLockType.Missile),
            3: DoorData(RoomName.Nursery_Access),
            4: DoorData(RoomName.Plaza_Access, tricks=[Tricks.vault_via_plaza]),
            5: DoorData(RoomName.Piston_Tunnel, rule_func=lambda state, player: False),  # Piston tunnel to training chamber is blocked by a chozo head that needs to be destroyed from the other side
        },
            pickups=[PickupData('Chozo Ruins: Main Plaza - Half-Pipe', rule_func=can_boost, tricks=[Tricks.plaza_half_pipe_no_boost]),
                     PickupData('Chozo Ruins: Main Plaza - Grapple Ledge', rule_func=lambda state, player: state.can_reach_region(RoomName.Piston_Tunnel.value, player) and can_grapple(state, player), tricks=[Tricks.plaza_grapple_ledge_r_jump]),
                     PickupData('Chozo Ruins: Main Plaza - Tree', rule_func=can_super_missile, tricks=[]),
                     PickupData('Chozo Ruins: Main Plaza - Locked Door', rule_func=lambda state, player: state.can_reach_region(RoomName.Plaza_Access.value, player) and can_morph_ball(state, player), tricks=[Tricks.vault_via_plaza]), ]),  # If we do room rando, the logic for this will need to be adjusted
        RoomName.Map_Station: RoomData(doors={}, pickups=[]),
        RoomName.Meditation_Fountain: RoomData(doors={
            0: DoorData(RoomName.Magma_Pool),
            1: DoorData(RoomName.Ruined_Fountain),
        }),
        RoomName.North_Atrium: RoomData(doors={
            0: DoorData(RoomName.Ruined_Nursery),
            1: DoorData(RoomName.Ruined_Gallery),
        }),
        RoomName.Nursery_Access: RoomData(doors={
            0: DoorData(RoomName.Eyon_Tunnel),
            1: DoorData(RoomName.Main_Plaza),
        }),
        RoomName.Piston_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Main_Plaza, rule_func=can_morph_ball),
            1: DoorData(RoomName.Training_Chamber, rule_func=can_morph_ball),
        }),
        RoomName.Plaza_Access: RoomData(doors={
            0: DoorData(RoomName.Main_Plaza),
            1: DoorData(RoomName.Vault),
        }),
        RoomName.Reflecting_Pool_Access: RoomData(doors={
            0: DoorData(RoomName.Reflecting_Pool),
            1: DoorData(RoomName.Hall_of_the_Elders),
        }),
        RoomName.Reflecting_Pool: RoomData(doors={
            0: DoorData(RoomName.Save_Station_3, defaultLock=DoorLockType.Missile, tricks=[Tricks.reflecting_pool_space_jump_climb]),
            1: DoorData(RoomName.Transport_Access_South, defaultLock=DoorLockType.Ice, tricks=[Tricks.reflecting_pool_space_jump_climb]),
            2: DoorData(RoomName.Reflecting_Pool_Access),
            3: DoorData(RoomName.Antechamber, defaultLock=DoorLockType.Missile, rule_func=lambda state, player: can_boost(state, player) and can_bomb(state, player), tricks=[Tricks.reflecting_pool_space_jump_climb]),
        }),
        RoomName.Ruined_Fountain_Access: RoomData(doors={
            0: DoorData(RoomName.Main_Plaza, rule_func=can_morph_ball),
            1: DoorData(RoomName.Ruined_Fountain, rule_func=can_morph_ball),
        }),
        RoomName.Ruined_Fountain: RoomData(
            doors={
                0: DoorData(RoomName.Arboretum_Access),
                1: DoorData(RoomName.Ruined_Fountain_Access),
                2: DoorData(RoomName.Meditation_Fountain),
            },
            pickups=[PickupData('Chozo Ruins: Ruined Fountain', rule_func=lambda state, player: can_flaahgra(state, player) and can_spider(state, player) and can_bomb(state, player))], ),  # This location can accidentally be locked out if flaaghra is skipped
        RoomName.Ruined_Gallery: RoomData(
            doors={
                0: DoorData(RoomName.North_Atrium),
                1: DoorData(RoomName.Totem_Access),
                2: DoorData(RoomName.Map_Station),
            },
            pickups=[
                PickupData('Chozo Ruins: Ruined Gallery - Missile Wall', rule_func=can_missile),
                PickupData('Chozo Ruins: Ruined Gallery - Tunnel', rule_func=can_bomb),
            ]),
        RoomName.Ruined_Nursery: RoomData(
            doors={
                0: DoorData(RoomName.Save_Station_1),
                1: DoorData(RoomName.North_Atrium),
                2: DoorData(RoomName.Eyon_Tunnel),
            },
            pickups=[PickupData('Chozo Ruins: Ruined Nursery', rule_func=can_bomb, tricks=[Tricks.ruined_nursery_no_bombs]), ]),
        RoomName.Ruined_Shrine_Access: RoomData(doors={
            0: DoorData(RoomName.Ruined_Shrine),
            1: DoorData(RoomName.Main_Plaza, defaultLock=DoorLockType.Missile),
        }),
        RoomName.Ruined_Shrine: RoomData(
            doors={
                0: DoorData(RoomName.Tower_of_Light_Access, defaultLock=DoorLockType.Wave,
                            rule_func=lambda state, player: can_spider(state, player) and can_boost(state, player),
                            tricks=[
                                Tricks.ruined_shrine_upper_door_no_spider_ball,
                                Tricks.ruined_shrine_upper_door_scan_dash
                            ]),
                1: DoorData(RoomName.Ruined_Shrine_Access, rule_func=lambda state, player: can_morph_ball(state, player) or can_space_jump(state, player), tricks=[Tricks.ruined_shrine_scan_dash_escape]),
            },
            pickups=[
                PickupData('Chozo Ruins: Ruined Shrine - Plated Beetle', rule_func=can_exit_ruined_shrine, tricks=[Tricks.ruined_shrine_scan_dash_escape]),
                PickupData('Chozo Ruins: Ruined Shrine - Half-Pipe', rule_func=can_boost),
                PickupData('Chozo Ruins: Ruined Shrine - Lower Tunnel', rule_func=lambda state, player: can_exit_ruined_shrine(state, player) and can_bomb(state, player), tricks=[Tricks.ruined_shrine_scan_dash_escape]),
            ]),
        RoomName.Ruins_Entrance: RoomData(doors={
            0: DoorData(RoomName.Main_Plaza),
            1: DoorData(RoomName.Transport_to_Tallon_Overworld_North),
        }),
        RoomName.Save_Station_1: RoomData(doors={0: DoorData(RoomName.Ruined_Nursery), }, pickups=[]),
        RoomName.Save_Station_2: RoomData(doors={
            0: DoorData(RoomName.Gathering_Hall, defaultLock=DoorLockType.Missile),
        }),
        RoomName.Save_Station_3: RoomData(doors={
            0: DoorData(RoomName.Reflecting_Pool, defaultLock=DoorLockType.Missile, rule_func=can_bomb),
            1: DoorData(RoomName.Transport_to_Tallon_Overworld_East, rule_func=can_bomb),
        }),
        RoomName.Sun_Tower: RoomData(doors={
            0: DoorData(RoomName.Sun_Tower_Access, rule_func=can_climb_sun_tower, exclude_from_rando=True),
            1: DoorData(RoomName.Transport_to_Magmoor_Caverns_North),
        }),
        RoomName.Sun_Tower_Access: RoomData(doors={
            0: DoorData(RoomName.Sunchamber, exclude_from_rando=True),
            1: DoorData(RoomName.Sun_Tower, exclude_from_rando=True),
        }),
        RoomName.Sunchamber_Access: RoomData(doors={
            0: DoorData(RoomName.Sunchamber),
            1: DoorData(RoomName.Sunchamber_Lobby),
        }, ),
        RoomName.Sunchamber_Lobby: RoomData(doors={
            0: DoorData(RoomName.Sunchamber_Access),
            1: DoorData(RoomName.Arboretum, defaultLock=DoorLockType.Missile,),
        }),
        RoomName.Sunchamber: RoomData(doors={
            0: DoorData(RoomName.Sun_Tower_Access, rule_func=can_flaahgra, exclude_from_rando=True)
            # 1: DoorData(RoomName.Sunchamber_Lobby, rule_func=can_climb_sun_tower) # gets locked until after you beat the ghosts
        }, pickups=[
            PickupData('Chozo Ruins: Sunchamber - Flaaghra', rule_func=can_flaahgra),
            PickupData('Chozo Ruins: Sunchamber - Ghosts', rule_func=lambda state, player: can_flaahgra(state, player) and can_climb_sun_tower(state, player))]),
        RoomName.Totem_Access: RoomData(doors={
            0: DoorData(RoomName.Ruined_Gallery),
            1: DoorData(RoomName.Hive_Totem),
        }),
        RoomName.Tower_Chamber: RoomData(doors={
            0: DoorData(RoomName.Tower_of_Light, defaultLock=DoorLockType.Wave),
        }, pickups=[PickupData('Chozo Ruins: Tower Chamber', rule_func=lambda state, player: True), ]),
        RoomName.Tower_of_Light_Access: RoomData(doors={
            0: DoorData(RoomName.Tower_of_Light),
            1: DoorData(RoomName.Ruined_Shrine),
        }),
        RoomName.Tower_of_Light: RoomData(
            doors={
                0: DoorData(RoomName.Tower_of_Light_Access, defaultLock=DoorLockType.Wave),
                1: DoorData(RoomName.Tower_Chamber, defaultLock=DoorLockType.Wave, rule_func=lambda state, player: can_move_underwater(state, player) and can_space_jump(state, player), tricks=[Tricks.tower_chamber_no_gravity]),
            },
            pickups=[
                PickupData('Chozo Ruins: Tower of Light',
                           rule_func=can_climb_tower_of_light,
                           tricks=[Tricks.tower_of_light_climb_without_missiles])]),
        RoomName.Training_Chamber_Access: RoomData(
            doors={
                0: DoorData(RoomName.Magma_Pool, defaultLock=DoorLockType.Wave),
                1: DoorData(RoomName.Training_Chamber, defaultLock=DoorLockType.Wave)
            },
            pickups=[PickupData('Chozo Ruins: Training Chamber Access', rule_func=can_morph_ball)]),
        RoomName.Training_Chamber: RoomData(
            doors={
                0: DoorData(RoomName.Training_Chamber_Access, defaultLock=DoorLockType.Wave),
                1: DoorData(RoomName.Piston_Tunnel, rule_func=lambda state, player: can_boost(state, player) and can_bomb(state, player))
            },
            pickups=[PickupData('Chozo Ruins: Training Chamber', rule_func=lambda state, player: can_boost(state, player) and can_spider(state, player) and can_bomb(state, player))]),
        RoomName.Transport_Access_North: RoomData(
            doors={
                0: DoorData(RoomName.Hive_Totem, defaultLock=DoorLockType.Missile, rule_func=can_bomb),
                1: DoorData(RoomName.Transport_to_Magmoor_Caverns_North, rule_func=can_morph_ball),
            },
            pickups=[PickupData('Chozo Ruins: Transport Access North')]),
        RoomName.Transport_Access_South: RoomData(doors={
            0: DoorData(RoomName.Reflecting_Pool, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Transport_to_Tallon_Overworld_South),
        }),
        RoomName.Transport_to_Magmoor_Caverns_North: RoomData(doors={
            0: DoorData(RoomName.Sun_Tower),
            1: DoorData(RoomName.Vault_Access),
            2: DoorData(RoomName.Transport_Access_North),
        }),
        RoomName.Transport_to_Tallon_Overworld_East: RoomData(doors={
            0: DoorData(RoomName.Save_Station_3),
        }),
        RoomName.Transport_to_Tallon_Overworld_North: RoomData(doors={
            0: DoorData(RoomName.Ruins_Entrance)
        }),
        RoomName.Transport_to_Tallon_Overworld_South: RoomData(doors={
            0: DoorData(RoomName.Transport_Access_South),
        }),
        RoomName.Vault_Access: RoomData(
            doors={
                0: DoorData(RoomName.Vault, rule_func=can_morph_ball),
                1: DoorData(RoomName.Transport_to_Magmoor_Caverns_North, rule_func=can_morph_ball),

            }),
        RoomName.Vault: RoomData(
            doors={
                0: DoorData(RoomName.Vault_Access),
                1: DoorData(RoomName.Plaza_Access),
            },
            pickups=[PickupData('Chozo Ruins: Vault', rule_func=can_bomb), ]),
        RoomName.Watery_Hall_Access: RoomData(
            doors={
                0: DoorData(RoomName.Gathering_Hall),
                1: DoorData(RoomName.Watery_Hall, defaultLock=DoorLockType.Missile),
            },
            pickups=[PickupData('Chozo Ruins: Watery Hall Access', rule_func=can_missile), ]),
        RoomName.Watery_Hall: RoomData(
            doors={
                0: DoorData(RoomName.Dynamo_Access, destinationArea=MetroidPrimeArea.Chozo_Ruins, defaultLock=DoorLockType.Missile, rule_func=lambda state, player: can_scan(state, player) and can_power_bomb(state, player)),
                1: DoorData(RoomName.Watery_Hall_Access, defaultLock=DoorLockType.Missile),

            },
            pickups=[
                PickupData('Chozo Ruins: Watery Hall - Scan Puzzle', rule_func=can_scan),
                PickupData('Chozo Ruins: Watery Hall - Underwater', rule_func=lambda state, player: can_move_underwater(state, player) and can_space_jump(state, player), tricks=[Tricks.watery_hall_no_gravity]),
            ]),
        RoomName.West_Furnace_Access: RoomData(doors={
            0: DoorData(RoomName.Energy_Core),
            1: DoorData(RoomName.Furnace, rule_func=lambda state, player: can_spider(state, player) and can_bomb(state, player), tricks=[Tricks.furnace_no_spider_ball]),
        }, pickups=[PickupData('Chozo Ruins: Furnace - Inside Furnace', rule_func=can_bomb),])  # This is not actually in west furnace but it can only be accessed from west furnace, logic-wise
    }
