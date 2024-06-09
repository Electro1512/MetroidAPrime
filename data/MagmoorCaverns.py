
from worlds.metroidprime.data.Tricks import Tricks
from .RoomData import AreaData, DoorData, DoorLockType, MetroidPrimeArea, PickupData, RoomData
from worlds.metroidprime.Logic2 import can_bomb, can_boost, can_grapple, can_heat, can_missile, can_morph_ball, can_move_underwater, can_plasma_beam, can_power_bomb, can_scan, can_space_jump, can_spider, can_thermal, can_wave_beam, can_xray, has_energy_tanks
from .RoomNames import RoomName


class MagmoorCavernsAreaData(AreaData):
    rooms = {
        RoomName.Burning_Trail: RoomData(doors={
            0: DoorData(RoomName.Lake_Tunnel),
            1: DoorData(RoomName.Transport_to_Chozo_Ruins_North),
            2: DoorData(RoomName.Save_Station_Magmoor_A, defaultLock=DoorLockType.Missile),
        }),
        RoomName.Fiery_Shores: RoomData(doors={
            0: DoorData(RoomName.Shore_Tunnel, rule_func=lambda state, player: can_heat(state, player) and (can_bomb(state, player) or can_grapple(state, player) or has_energy_tanks(state, player, 4))),
            1: DoorData(RoomName.Transport_Tunnel_B, destinationArea=MetroidPrimeArea.Magmoor_Caverns, rule_func=lambda state, player: can_heat(state, player) and (can_bomb(state, player) or can_grapple(state, player))),
            # 2: DoorData(RoomName.Warrior_Shrine, rule_func=lambda state, player: False), Can't access, one way trip
        }, pickups=[
            PickupData('Magmoor Caverns: Fiery Shores - Morph Track', tricks=[Tricks.fiery_shores_morphball_track_sj], rule_func=can_bomb),
            PickupData('Magmoor Caverns: Fiery Shores - Warrior Shrine Tunnel', rule_func=lambda state, player:  can_power_bomb(state, player) and can_bomb(state, player) and state.can_reach(RoomName.Warrior_Shrine.value, None, player))  # Not an item in this room but can only be accessed from here
        ]),
        RoomName.Geothermal_Core: RoomData(doors={
            0: DoorData(RoomName.North_Core_Tunnel, rule_func=can_space_jump),
            1: DoorData(RoomName.Plasma_Processing, defaultLock=DoorLockType.Ice,
                        rule_func=lambda state, player: can_bomb(state, player) and can_boost(state, player) and can_grapple(state, player) and can_spider(state, player) and can_space_jump(state, player),
                        tricks=[Tricks.geothermal_core_no_grapple_spider]
                        ),
            2: DoorData(RoomName.South_Core_Tunnel, rule_func=can_space_jump),
        }),
        RoomName.Lake_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Lava_Lake, rule_func=can_heat, tricks=[Tricks.lava_lake_item_suitless]),
            1: DoorData(RoomName.Burning_Trail, rule_func=can_heat, tricks=[Tricks.lava_lake_item_suitless]),
        }),
        RoomName.Lava_Lake: RoomData(
            doors={
                0: DoorData(RoomName.Lake_Tunnel, rule_func=lambda state, player: can_heat(state, player) and (can_bomb(state, player) or can_power_bomb(state, player)), tricks=[Tricks.lava_lake_item_suitless]),
                1: DoorData(RoomName.Pit_Tunnel, rule_func=lambda state, player: can_heat(state, player) and (can_bomb(state, player) or can_power_bomb(state, player)), tricks=[Tricks.lava_lake_item_suitless]),
            },
            pickups=[PickupData('Magmoor Caverns: Lava Lake', rule_func=lambda state, player: can_missile(state, player) and can_space_jump(state, player),  tricks=[Tricks.lava_lake_item_missiles_only, Tricks.lava_lake_item_suitless]), ]),
        RoomName.Magmoor_Workstation: RoomData(
            doors={
                0: DoorData(RoomName.South_Core_Tunnel),
                1: DoorData(RoomName.Workstation_Tunnel, rule_func=can_space_jump),
                2: DoorData(RoomName.Transport_Tunnel_C, defaultLock=DoorLockType.Wave, destinationArea=MetroidPrimeArea.Magmoor_Caverns, rule_func=can_space_jump),
            },
            pickups=[PickupData('Magmoor Caverns: Magmoor Workstation', rule_func=lambda state, player: can_thermal(state, player) and can_wave_beam(state, player) and can_scan(state, player) and can_morph_ball(state, player),
                                tricks=[Tricks.magmoor_workstation_no_thermal]), ]),
        RoomName.Monitor_Station: RoomData(doors={
            0: DoorData(RoomName.Monitor_Tunnel, rule_func=can_heat),
            1: DoorData(RoomName.Transport_Tunnel_A, rule_func=can_heat, destinationArea=MetroidPrimeArea.Magmoor_Caverns),
            2: DoorData(RoomName.Warrior_Shrine, rule_func=lambda state, player: can_heat(state, player) and can_space_jump(state, player) and can_boost(state, player), tricks=[Tricks.warrior_shrine_no_boost, Tricks.warrior_shrine_minimal_reqs]),
            3: DoorData(RoomName.Shore_Tunnel, rule_func=can_heat),
        }),
        RoomName.Monitor_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Monitor_Station, rule_func=can_heat),
            1: DoorData(RoomName.Triclops_Pit, rule_func=can_heat),
        }),
        RoomName.North_Core_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Twin_Fires, defaultLock=DoorLockType.Wave, rule_func=can_space_jump),
            1: DoorData(RoomName.Geothermal_Core, defaultLock=DoorLockType.Wave, rule_func=can_space_jump),
        }),
        RoomName.Pit_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Triclops_Pit, rule_func=lambda state, player: can_heat(state, player) and (can_morph_ball(state, player) or can_space_jump(state, player))),
            1: DoorData(RoomName.Lava_Lake,  rule_func=lambda state, player: can_heat(state, player) and (can_morph_ball(state, player) or can_space_jump(state, player))),
        }),
        RoomName.Plasma_Processing: RoomData(doors={
            0: DoorData(RoomName.Geothermal_Core, defaultLock=DoorLockType.Plasma),
        }, pickups=[PickupData('Magmoor Caverns: Plasma Processing', rule_func=can_plasma_beam)]),  # Requires plasma beam to exit
        RoomName.Save_Station_Magmoor_A: RoomData(doors={
            0: DoorData(RoomName.Burning_Trail, defaultLock=DoorLockType.Missile),
        }),
        RoomName.Save_Station_Magmoor_B: RoomData(doors={
            0: DoorData(RoomName.Transport_to_Phendrana_Drifts_South, defaultLock=DoorLockType.Missile),
        }),
        RoomName.Shore_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Monitor_Station, rule_func=can_heat),
            1: DoorData(RoomName.Fiery_Shores, rule_func=can_heat),
        }, pickups=[PickupData('Magmoor Caverns: Shore Tunnel', rule_func=lambda state, player: can_power_bomb(state, player) and can_space_jump(state, player), tricks=[Tricks.shore_tunnel_escape_no_sj]), ],),
        RoomName.South_Core_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Geothermal_Core, defaultLock=DoorLockType.Wave, rule_func=can_space_jump),
            1: DoorData(RoomName.Magmoor_Workstation, defaultLock=DoorLockType.Wave, rule_func=can_space_jump),
        }),
        RoomName.Storage_Cavern: RoomData(doors={0: DoorData(RoomName.Triclops_Pit, rule_func=can_heat), }, pickups=[PickupData('Magmoor Caverns: Storage Cavern'), ]),
        RoomName.Transport_to_Chozo_Ruins_North: RoomData(doors={
            0: DoorData(RoomName.Burning_Trail),
        }),
        RoomName.Transport_to_Phazon_Mines_West: RoomData(doors={
            0: DoorData(RoomName.Workstation_Tunnel, defaultLock=DoorLockType.Ice),
        }),
        RoomName.Transport_to_Phendrana_Drifts_North: RoomData(doors={
            0: DoorData(RoomName.Transport_Tunnel_A, destinationArea=MetroidPrimeArea.Magmoor_Caverns),
        }),
        RoomName.Transport_to_Phendrana_Drifts_South: RoomData(doors={
            0: DoorData(RoomName.Save_Station_Magmoor_B, defaultLock=DoorLockType.Missile, exclude_from_rando=True),  # Door 1 is not annotated, not sure which one is which
            1: DoorData(RoomName.Transport_Tunnel_C, destinationArea=MetroidPrimeArea.Magmoor_Caverns, defaultLock=DoorLockType.Wave, exclude_from_rando=True),
        }),
        RoomName.Transport_to_Tallon_Overworld_West: RoomData(doors={
            0: DoorData(RoomName.Twin_Fires_Tunnel),
            1: DoorData(RoomName.Transport_Tunnel_B, destinationArea=MetroidPrimeArea.Magmoor_Caverns),
        }),
        RoomName.Transport_Tunnel_A: RoomData(doors={
            0: DoorData(RoomName.Transport_to_Phendrana_Drifts_North, rule_func=lambda state, player: can_heat(state, player) and can_bomb(state, player)),
            1: DoorData(RoomName.Monitor_Station, rule_func=lambda state, player: can_heat(state, player) and can_bomb(state, player)),
        }, pickups=[PickupData('Magmoor Caverns: Transport Tunnel A', rule_func=can_bomb)], area=MetroidPrimeArea.Magmoor_Caverns),
        RoomName.Transport_Tunnel_B: RoomData(doors={
            0: DoorData(RoomName.Transport_to_Tallon_Overworld_West, rule_func=lambda state, player: can_heat(state, player) and (can_morph_ball(state, player) or has_energy_tanks(state, player, 3))),
            1: DoorData(RoomName.Fiery_Shores, rule_func=lambda state, player: can_heat(state, player) and (can_morph_ball(state, player) or has_energy_tanks(state, player, 3))),
        }, area=MetroidPrimeArea.Magmoor_Caverns),
        RoomName.Transport_Tunnel_C: RoomData(doors={
            0: DoorData(RoomName.Transport_to_Phendrana_Drifts_South, defaultLock=DoorLockType.Wave),
            1: DoorData(RoomName.Magmoor_Workstation, defaultLock=DoorLockType.Wave),
        }, area=MetroidPrimeArea.Magmoor_Caverns),
        RoomName.Triclops_Pit: RoomData(
            doors={
                0: DoorData(RoomName.Monitor_Tunnel, rule_func=lambda state, player: can_heat(state, player)),
                1: DoorData(RoomName.Storage_Cavern, rule_func=lambda state, player: can_heat(state, player) and can_morph_ball(state, player)),
                2: DoorData(RoomName.Pit_Tunnel, rule_func=lambda state, player: can_heat(state, player)),
            },
            pickups=[PickupData('Magmoor Caverns: Triclops Pit', rule_func=lambda state, player: can_xray(state, player) and can_space_jump(state, player) and can_missile(state, player),
                                tricks=[
                Tricks.triclops_pit_item_no_missiles,
                Tricks.triclops_pit_item_no_sj,
                Tricks.triclops_pit_item_no_xray,
                Tricks.triclops_pit_item_no_sj_no_xray,
            ]), ]),
        RoomName.Twin_Fires_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Twin_Fires, rule_func=lambda state, player: can_heat(state, player) and can_spider(state, player), tricks=[Tricks.twin_fires_tunnel_no_spider, Tricks.cross_twin_fires_suitless]),
            1: DoorData(RoomName.Transport_to_Tallon_Overworld_West, rule_func=lambda state, player: can_heat(state, player) and (can_spider(state, player) or has_energy_tanks(state, player, 4 and (can_move_underwater(state, player) or can_space_jump(state, player))))),  # Can't jump out of the lava without gravity or sj
        }),
        RoomName.Twin_Fires: RoomData(doors={
            0: DoorData(RoomName.North_Core_Tunnel, defaultLock=DoorLockType.Wave, rule_func=lambda state, player: (can_space_jump(state, player) and has_energy_tanks(state, player, 2)) or can_grapple(state, player)),
            1: DoorData(RoomName.Twin_Fires_Tunnel, rule_func=lambda state, player: (can_space_jump(state, player) and has_energy_tanks(state, player, 2)) or can_grapple(state, player)),
        }),
        RoomName.Warrior_Shrine: RoomData(doors={
            0: DoorData(RoomName.Monitor_Station, rule_func=lambda state, player: can_heat(state, player)),
            1: DoorData(RoomName.Fiery_Shores, defaultLock=DoorLockType.None_, rule_func=lambda state, player: can_heat(state, player) and can_power_bomb(state, player) and can_bomb(state, player), exclude_from_rando=True),
        }, pickups=[PickupData('Magmoor Caverns: Warrior Shrine')]),
        RoomName.Workstation_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Transport_to_Phazon_Mines_West, rule_func=can_power_bomb, defaultLock=DoorLockType.Ice),
            1: DoorData(RoomName.Magmoor_Workstation, rule_func=can_power_bomb),
        })
    }
