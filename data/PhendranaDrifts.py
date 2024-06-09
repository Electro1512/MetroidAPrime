
from worlds.metroidprime.data.Tricks import Tricks
from .RoomData import AreaData, DoorData, DoorLockType, MetroidPrimeArea, PickupData, RoomData
from worlds.metroidprime.Logic2 import can_bomb, can_boost, can_charge_beam, can_climb_sun_tower, can_climb_tower_of_light, can_defeat_sheegoth, can_exit_ruined_shrine, can_flaahgra, can_grapple, can_heat, can_ice_beam, can_melt_ice, can_missile, can_morph_ball, can_move_underwater, can_plasma_beam, can_power_bomb, can_scan, can_space_jump, can_spider, can_super_missile, can_thermal, can_wave_beam, can_xray, has_energy_tanks
from .RoomNames import RoomName


class PhendranaDriftsAreaData(AreaData):
    rooms = {
        RoomName.Aether_Lab_Entryway: RoomData(doors={}),
        RoomName.Canyon_Entryway: RoomData(doors={}),
        RoomName.Chamber_Access: RoomData(doors={}),
        RoomName.Chapel_of_the_Elders: RoomData(doors={
            0: DoorData(RoomName.Chapel_Tunnel, defaultLock=DoorLockType.Wave, rule_func=lambda state, player: can_defeat_sheegoth(state, player) and can_space_jump(state, player) and can_wave_beam(state, player), tricks=[Tricks.chapel_of_elders_escape_no_sj]),
        }, pickups=[PickupData('Phendrana Drifts: Chapel of the Elders', tricks=[Tricks.chapel_of_elders_escape_no_sj]), ]),
        RoomName.Chapel_Tunnel: RoomData(doors={
            0: DoorData(RoomName.Chapel_of_the_Elders, rule_func=lambda state, player: can_bomb(state, player)),
            1: DoorData(RoomName.Chozo_Ice_Temple, rule_func=lambda state, player: can_bomb(state, player)),
        }),
        RoomName.Chozo_Ice_Temple: RoomData(doors={
            0: DoorData(RoomName.Temple_Entryway),
            1: DoorData(RoomName.Chapel_Tunnel, rule_func=lambda state, player: can_bomb(state, player) and can_space_jump(state, player), tricks=[Tricks.ice_temple_no_sj]),
        },
            pickups=[PickupData('Phendrana Drifts: Chozo Ice Temple', rule_func=lambda state, player: can_morph_ball(state, player) and can_space_jump(state, player) and can_melt_ice(state, player), tricks=[]), ]),
        RoomName.Control_Tower: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Control Tower', tricks=[]), ]),
        RoomName.Courtyard_Entryway: RoomData(doors={}),
        RoomName.East_Tower: RoomData(doors={}),
        RoomName.Frost_Cave_Access: RoomData(doors={}),
        RoomName.Frost_Cave: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Frost Cave', tricks=[]), ]),
        RoomName.Frozen_Pike: RoomData(doors={}),
        RoomName.Gravity_Chamber: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Gravity Chamber - Underwater', tricks=[]), PickupData('Phendrana Drifts: Gravity Chamber - Grapple Ledge', tricks=[]), ]),
        RoomName.Hunter_Cave_Access: RoomData(doors={}),
        RoomName.Hunter_Cave: RoomData(doors={}),
        RoomName.Hydra_Lab_Entryway: RoomData(doors={}),
        RoomName.Ice_Ruins_Access: RoomData(doors={
            0: DoorData(RoomName.Ice_Ruins_East, rule_func=lambda state, player: can_missile(state, player) or can_charge_beam(state, player)),
            1: DoorData(RoomName.Phendrana_Shorelines, rule_func=lambda state, player: can_missile(state, player) or can_charge_beam(state, player)),
        }),
        RoomName.Ice_Ruins_East: RoomData(
            doors={
                0: DoorData(RoomName.Ice_Ruins_Access),
                1: DoorData(RoomName.Plaza_Walkway),
            },
            pickups=[
                PickupData('Phendrana Drifts: Ice Ruins East - Behind Ice', rule_func=can_melt_ice, tricks=[]),
                PickupData('Phendrana Drifts: Ice Ruins East - Spider Track', rule_func=can_spider, tricks=[]),
            ]),
        RoomName.Ice_Ruins_West: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Ice Ruins West', tricks=[]), ]),
        RoomName.Lake_Tunnel: RoomData(doors={}),
        RoomName.Lower_Edge_Tunnel: RoomData(doors={}),
        RoomName.Map_Station: RoomData(doors={}),
        RoomName.North_Quarantine_Tunnel: RoomData(doors={}),
        RoomName.Observatory_Access: RoomData(doors={}),
        RoomName.Observatory: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Observatory', tricks=[]), ]),
        RoomName.Phendrana_Canyon: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Phendrana Canyon', tricks=[]), ]),
        RoomName.Phendrana_Shorelines: RoomData(
            doors={
                0: DoorData(RoomName.Shoreline_Entrance),
                1: DoorData(RoomName.Temple_Entryway, rule_func=can_space_jump, tricks=[Tricks.ice_temple_no_sj]),
                2: DoorData(RoomName.Save_Station_B),
                3: DoorData(RoomName.Ruins_Entryway, rule_func=can_space_jump),
                4: DoorData(RoomName.Plaza_Walkway, rule_func=can_space_jump),
                5: DoorData(RoomName.Ice_Ruins_Access, rule_func=lambda state, player: can_missile(state, player) and can_scan(state, player)),
            },
            pickups=[
                PickupData('Phendrana Drifts: Phendrana Shorelines - Behind Ice', rule_func=can_melt_ice, tricks=[]),
                PickupData('Phendrana Drifts: Phendrana Shorelines - Spider Track', rule_func=lambda state, player: can_bomb(state, player) and can_spider(state, player) and can_super_missile(state, player) and can_scan(state, player) and can_space_jump(state, player), tricks=[Tricks.shorelines_spider_track_no_sj]),
            ]),
        RoomName.Phendranas_Edge: RoomData(doors={}),
        RoomName.Pike_Access: RoomData(doors={}),
        RoomName.Plaza_Walkway: RoomData(doors={
            0: DoorData(RoomName.Phendrana_Shorelines),
            1: DoorData(RoomName.Ice_Ruins_East),
            2: DoorData(RoomName.Ruins_Entryway, exclude_from_rando=True),  # Entryway via shoreline
        }),
        RoomName.Quarantine_Access: RoomData(doors={}),
        RoomName.Quarantine_Cave: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Quarantine Cave', tricks=[]), ]),
        RoomName.Quarantine_Monitor: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Quarantine Monitor', tricks=[]), ]),
        RoomName.Research_Core_Access: RoomData(doors={}),
        RoomName.Research_Core: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Research Core', tricks=[]), ]),
        RoomName.Research_Entrance: RoomData(doors={}),
        RoomName.Research_Lab_Aether: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Research Lab Aether - Tank', tricks=[]), PickupData('Phendrana Drifts: Research Lab Aether - Morph Track', tricks=[]), ]),
        RoomName.Research_Lab_Hydra: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Research Lab Hydra', tricks=[]), ]),
        RoomName.Ruined_Courtyard: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Ruined Courtyard', tricks=[]), ]),
        RoomName.Ruins_Entryway: RoomData(doors={
            # TODO: Impl
            2: DoorData(RoomName.Plaza_Walkway, exclude_from_rando=True),  # Walkway via shoreline
        }),
        RoomName.Save_Station_A: RoomData(doors={}),
        RoomName.Save_Station_B: RoomData(doors={}),
        RoomName.Save_Station_C: RoomData(doors={}),
        RoomName.Save_Station_D: RoomData(doors={}),
        RoomName.Security_Cave: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Security Cave', tricks=[]), ]),
        RoomName.Shoreline_Entrance: RoomData(doors={
            0: DoorData(RoomName.Transport_to_Magmoor_Caverns_West, rule_func=lambda state, player: can_charge_beam(state, player) or can_missile(state, player)),
            1: DoorData(RoomName.Phendrana_Shorelines, rule_func=lambda state, player: can_charge_beam(state, player) or can_missile(state, player)),
        }),
        RoomName.South_Quarantine_Tunnel: RoomData(doors={}),
        RoomName.Specimen_Storage: RoomData(doors={}),
        RoomName.Storage_Cave: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Storage Cave', tricks=[]), ]),
        RoomName.Temple_Entryway: RoomData(doors={
            0: DoorData(RoomName.Chozo_Ice_Temple, rule_func=lambda state, player: can_missile(state, player) or can_charge_beam(state, player)),
            1: DoorData(RoomName.Phendrana_Shorelines, rule_func=lambda state, player: can_missile(state, player) or can_charge_beam(state, player)),
        }),
        RoomName.Transport_Access: RoomData(doors={}, pickups=[PickupData('Phendrana Drifts: Transport Access', tricks=[]), ]),
        RoomName.Transport_to_Magmoor_Caverns_South: RoomData(doors={}),
        RoomName.Transport_to_Magmoor_Caverns_West: RoomData(doors={
            0: DoorData(RoomName.Shoreline_Entrance),
        }),
        RoomName.Upper_Edge_Tunnel: RoomData(doors={}),
        RoomName.West_Tower_Entrance: RoomData(doors={}),
        RoomName.West_Tower: RoomData(doors={})
    }
