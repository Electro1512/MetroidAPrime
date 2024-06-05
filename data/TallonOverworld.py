
from worlds.metroidprime.Logic2 import can_bomb, can_boost, can_charge_beam, can_crashed_frigate, can_grapple, can_missile, can_morph_ball, can_move_underwater, can_power_bomb, can_space_jump, can_spider, can_super_missile, can_xray
from worlds.metroidprime.data.Tricks import Tricks
from .RoomData import AreaData, DoorData, DoorLockType, MetroidPrimeArea, PickupData, RoomData
from .RoomNames import RoomName


class TallonOverworldAreaData(AreaData):
    rooms = {

        RoomName.Alcove: RoomData(
            doors={
                0: DoorData(RoomName.Landing_Site,
                            rule_func=can_space_jump,
                            tricks=[Tricks.alcove_escape]),
                1: DoorData(RoomName.Gully, exclude_from_rando=True),  # Gully Via Landing Site
            },
            pickups=[
                PickupData('Tallon Overworld: Alcove'),
            ]),

        RoomName.Arbor_Chamber: RoomData(
            doors={
                0: DoorData(RoomName.Root_Cave),
            },
            pickups=[
                PickupData('Tallon Overworld: Arbor Chamber'),
            ]),

        RoomName.Artifact_Temple: RoomData(
            doors={
                0: DoorData(RoomName.Temple_Lobby),
            },
            pickups=[
                PickupData('Tallon Overworld: Artifact Temple'),
            ]),

        RoomName.Biohazard_Containment: RoomData(
            doors={
                0: DoorData(RoomName.Cargo_Freight_Lift_to_Deck_Gamma, rule_func=can_crashed_frigate, tricks=[Tricks.frigate_no_gravity]),
                1: DoorData(RoomName.Hydro_Access_Tunnel, rule_func=can_crashed_frigate, tricks=[Tricks.frigate_no_gravity]),
            },
            pickups=[
                PickupData('Tallon Overworld: Biohazard Containment', rule_func=can_super_missile),
            ]),

        # RoomName.Biotech_Research_Area_1: RoomData(
        # ),

        RoomName.Canyon_Cavern: RoomData(
            doors={
                1: DoorData(RoomName.Landing_Site),
                0: DoorData(RoomName.Tallon_Canyon),
            },
        ),

        RoomName.Cargo_Freight_Lift_to_Deck_Gamma: RoomData(
            doors={
                0: DoorData(RoomName.Frigate_Crash_Site, defaultLock=DoorLockType.Ice,
                            rule_func=can_crashed_frigate,
                            tricks=[Tricks.frigate_no_gravity]),
                1: DoorData(RoomName.Biohazard_Containment,
                            rule_func=can_crashed_frigate,
                            tricks=[Tricks.frigate_no_gravity]),
            },
            pickups=[
                PickupData('Tallon Overworld: Cargo Freight Lift to Deck Gamma', rule_func=lambda state, player: can_missile(state, player) or can_charge_beam(state, player)),
            ]),

        # RoomName.Connection_Elevator_to_Deck_Beta: RoomData(
        # ),

        # RoomName.Deck_Beta_Conduit_Hall: RoomData(
        # ),

        # RoomName.Deck_Beta_Security_Hall: RoomData(
        # ),

        # RoomName.Deck_Beta_Transit_Hall: RoomData(
        # ),

        # RoomName.Frigate_Access_Tunnel: RoomData(
        # ),

        RoomName.Frigate_Crash_Site: RoomData(
            doors={
                0: DoorData(RoomName.Waterfall_Cavern, rule_func=can_missile),
                1: DoorData(RoomName.Cargo_Freight_Lift_to_Deck_Gamma, defaultLock=DoorLockType.Ice,
                            rule_func=can_crashed_frigate,
                            tricks=[Tricks.frigate_crash_site_slope_jump],
                            exclude_from_rando=True
                            ),
                2: DoorData(RoomName.Overgrown_Cavern, defaultLock=DoorLockType.Ice,
                            rule_func=lambda state, player: False,  # Can't reach unless a trick is used
                            tricks=[Tricks.frigate_crash_site_climb_to_overgrown_cavern]
                            ),
            },
            pickups=[
                PickupData('Tallon Overworld: Frigate Crash Site',
                           rule_func=lambda state, player: can_space_jump(state, player) and can_move_underwater(state, player),
                           tricks=[
                               Tricks.frigate_crash_site_scan_dash,
                               Tricks.frigate_crash_site_slope_jump
                           ]
                           ),
            ]),

        RoomName.Great_Tree_Chamber: RoomData(
            doors={
                0: DoorData(RoomName.Great_Tree_Hall),
            },
            pickups=[
                PickupData('Tallon Overworld: Great Tree Chamber'),
            ]),

        RoomName.Great_Tree_Hall: RoomData(
            doors={
                0: DoorData(RoomName.Hydro_Access_Tunnel, rule_func=lambda state, player: False, tricks=[Tricks.great_tree_hall_skip_bars]),  # Can't reach from other doors unless you use a trick until after you go through frigate
                1: DoorData(RoomName.Great_Tree_Chamber, rule_func=lambda state, player: can_xray(state, player) and can_space_jump(state, player), tricks=[Tricks.great_tree_chamber_no_xray]),
                2: DoorData(RoomName.Transport_Tunnel_D, defaultLock=DoorLockType.Ice),  # Can't reach from other doors unless you use a trick until after you go through frigate
                3: DoorData(RoomName.Life_Grove_Tunnel, defaultLock=DoorLockType.Ice,
                            rule_func=can_spider,
                            tricks=[Tricks.great_tree_hall_no_spider_ball]
                            ),
                4: DoorData(RoomName.Transport_Tunnel_E, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: False, tricks=[Tricks.great_tree_hall_skip_bars]),  # Can't reach from other doors unless you use a trick until after you go through frigate
            },
        ),

        RoomName.Gully: RoomData(
            doors={
                0: DoorData(RoomName.Tallon_Canyon, defaultLock=DoorLockType.Bomb, exclude_from_rando=True, rule_func=lambda state, player: can_bomb(state, player) and can_space_jump(state, player)),
                1: DoorData(RoomName.Alcove, exclude_from_rando=True)  # Alcove Via Landing Site
            },
        ),

        RoomName.Hydro_Access_Tunnel: RoomData(
            doors={
                0: DoorData(RoomName.Great_Tree_Hall, rule_func=lambda state, player: can_bomb(state, player) and can_move_underwater(state, player) and can_boost(state, player)),  # Boost is needed to open way in great tree hall
                1: DoorData(RoomName.Biohazard_Containment, rule_func=lambda state, player: can_bomb(state, player) and can_move_underwater(state, player),
                            tricks=[Tricks.frigate_no_gravity]),

                # This one isn't an actual door but is instead accounting for not being able to access the great tree hall lower from upper
                2: DoorData(RoomName.Transport_Tunnel_E, destinationArea=MetroidPrimeArea.Tallon_Overworld, defaultLock=DoorLockType.Ice, rule_func=can_space_jump, exclude_from_rando=True),
            },
            pickups=[
                PickupData('Tallon Overworld: Hydro Access Tunnel', rule_func=lambda state, player: can_bomb(state, player) and can_move_underwater(state, player)),
            ]),

        RoomName.Landing_Site: RoomData(
            doors={
                0: DoorData(RoomName.Gully, rule_func=lambda state, player: can_space_jump(state, player), tricks=[Tricks.landing_site_scan_dash]),
                1: DoorData(RoomName.Canyon_Cavern),
                2: DoorData(RoomName.Temple_Hall),
                3: DoorData(RoomName.Alcove, rule_func=can_space_jump, tricks=[Tricks.landing_site_scan_dash]),
                4: DoorData(RoomName.Waterfall_Cavern),
            },
            pickups=[
                PickupData('Tallon Overworld: Landing Site', rule_func=can_morph_ball),
            ]),

        RoomName.Life_Grove_Tunnel: RoomData(
            doors={
                0: DoorData(RoomName.Great_Tree_Hall, defaultLock=DoorLockType.Ice, rule_func=lambda state, player: can_power_bomb(state, player) and can_boost(state, player), exclude_from_rando=True),
                1: DoorData(RoomName.Life_Grove, defaultLock=DoorLockType.None_, rule_func=lambda state, player: can_power_bomb(state, player) and can_boost(state, player), exclude_from_rando=True)
            },
            pickups=[
                PickupData('Tallon Overworld: Life Grove Tunnel', rule_func=lambda state, player: can_bomb(state, player) and can_boost(state, player)),
            ]),

        RoomName.Life_Grove: RoomData(
            doors={
                0: DoorData(RoomName.Life_Grove_Tunnel, defaultLock=DoorLockType.None_,
                            rule_func=lambda state, player: can_power_bomb(state, player) and can_space_jump(state, player) and can_xray(state, player) and can_boost(state, player),
                            tricks=[],
                            exclude_from_rando=True)},
            pickups=[
                PickupData('Tallon Overworld: Life Grove - Start'), PickupData('Tallon Overworld: Life Grove - Underwater Spinner', rule_func=lambda state, player: can_boost(state, player) and can_bomb(state, player)),
            ]),

        # These have door types not in room data and no pickups
        # RoomName.Main_Ventilation_Shaft_Section_A: RoomData(
        # ),

        # RoomName.Main_Ventilation_Shaft_Section_B: RoomData(
        # ),

        # RoomName.Main_Ventilation_Shaft_Section_C: RoomData(
        # ),

        # RoomName.Reactor_Core: RoomData(
        # ),

        RoomName.Overgrown_Cavern: RoomData(
            doors={
                0: DoorData(RoomName.Frigate_Crash_Site, defaultLock=DoorLockType.Ice, rule_func=can_morph_ball),
                1: DoorData(RoomName.Transport_Tunnel_C, destinationArea=MetroidPrimeArea.Tallon_Overworld, defaultLock=DoorLockType.Ice, rule_func=can_morph_ball),
            },
            pickups=[
                PickupData('Tallon Overworld: Overgrown Cavern', rule_func=can_morph_ball),
            ]),

        # RoomName.Reactor_Access: RoomData(
        # ),

        RoomName.Root_Cave: RoomData(
            doors={
                0: DoorData(RoomName.Transport_Tunnel_B, destinationArea=MetroidPrimeArea.Tallon_Overworld),
                1: DoorData(RoomName.Root_Tunnel),
                2: DoorData(RoomName.Arbor_Chamber, defaultLock=DoorLockType.Plasma,
                            rule_func=lambda state, player: can_grapple(state, player) and can_xray(state, player) and can_space_jump(state, player),
                            tricks=[Tricks.root_cave_arbor_chamber_no_grapple_xray]
                            ),

            },
            pickups=[
                PickupData('Tallon Overworld: Root Cave'),
            ]),

        RoomName.Root_Tunnel: RoomData(
            doors={
                0: DoorData(RoomName.Root_Cave, defaultLock=DoorLockType.Missile),
                1: DoorData(RoomName.Tallon_Canyon),
            },
        ),

        # RoomName.Savestation: RoomData(
        # ),

        RoomName.Tallon_Canyon: RoomData(
            doors={
                0: DoorData(RoomName.Canyon_Cavern),
                1: DoorData(RoomName.Transport_Tunnel_A, destinationArea=MetroidPrimeArea.Tallon_Overworld),
                2: DoorData(RoomName.Gully, defaultLock=DoorLockType.Bomb, rule_func=lambda state, player: can_space_jump(state, player) or (can_boost(state, player) and can_bomb(state, player))),
                3: DoorData(RoomName.Root_Tunnel)
            }
        ),

        RoomName.Temple_Hall: RoomData(
            doors={
                1: DoorData(RoomName.Landing_Site),
                2: DoorData(RoomName.Temple_Security_Station),
            },
        ),

        RoomName.Temple_Lobby: RoomData(
            doors={
                0: DoorData(RoomName.Artifact_Temple),
                1: DoorData(RoomName.Temple_Security_Station),
            },
        ),

        RoomName.Temple_Security_Station: RoomData(
            doors={
                0: DoorData(RoomName.Temple_Hall),
                1: DoorData(RoomName.Temple_Lobby, defaultLock=DoorLockType.Missile),
            },
        ),

        RoomName.Transport_to_Chozo_Ruins_East: RoomData(
            doors={
                0: DoorData(RoomName.Transport_Tunnel_C, destinationArea=MetroidPrimeArea.Tallon_Overworld, defaultLock=DoorLockType.Ice),
            },
        ),

        RoomName.Transport_to_Chozo_Ruins_South: RoomData(
            doors={
                0: DoorData(RoomName.Transport_Tunnel_D, defaultLock=DoorLockType.Ice),
            },
        ),

        RoomName.Transport_to_Chozo_Ruins_West: RoomData(
            doors={
                0: DoorData(RoomName.Transport_Tunnel_A, destinationArea=MetroidPrimeArea.Tallon_Overworld),
            },
        ),

        RoomName.Transport_to_Magmoor_Caverns_East: RoomData(
            doors={
                0: DoorData(RoomName.Transport_Tunnel_B, destinationArea=MetroidPrimeArea.Tallon_Overworld)
            },
        ),

        RoomName.Transport_to_Phazon_Mines_East: RoomData(
            doors={
                0: DoorData(RoomName.Transport_Tunnel_E, defaultLock=DoorLockType.Ice),
            },
        ),

        RoomName.Transport_Tunnel_A: RoomData(
            doors={
                0: DoorData(RoomName.Transport_to_Chozo_Ruins_West),
                1: DoorData(RoomName.Tallon_Canyon),
            },
            area=MetroidPrimeArea.Tallon_Overworld,
        ),

        RoomName.Transport_Tunnel_B: RoomData(
            doors={
                0: DoorData(RoomName.Transport_to_Magmoor_Caverns_East),
                1: DoorData(RoomName.Root_Cave)
            },
            area=MetroidPrimeArea.Tallon_Overworld,
            pickups=[
                PickupData('Tallon Overworld: Transport Tunnel B'),
            ]),

        RoomName.Transport_Tunnel_C: RoomData(
            area=MetroidPrimeArea.Tallon_Overworld,
            doors={
                0: DoorData(RoomName.Overgrown_Cavern, defaultLock=DoorLockType.Ice),
                1: DoorData(RoomName.Transport_to_Chozo_Ruins_East, defaultLock=DoorLockType.Ice),
            },
        ),

        RoomName.Transport_Tunnel_D: RoomData(
            area=MetroidPrimeArea.Tallon_Overworld,

            doors={
                0: DoorData(RoomName.Great_Tree_Hall, defaultLock=DoorLockType.Ice),
                1: DoorData(RoomName.Transport_to_Chozo_Ruins_South, defaultLock=DoorLockType.Ice),
            },
        ),

        RoomName.Transport_Tunnel_E: RoomData(
            area=MetroidPrimeArea.Tallon_Overworld,
            doors={
                0: DoorData(RoomName.Transport_to_Phazon_Mines_East, defaultLock=DoorLockType.Ice),
                1: DoorData(RoomName.Great_Tree_Hall, defaultLock=DoorLockType.Ice),
            },
        ),

        RoomName.Waterfall_Cavern: RoomData(
            doors={
                0: DoorData(RoomName.Landing_Site, rule_func=can_morph_ball),
                1: DoorData(RoomName.Tallon_Canyon, defaultLock=DoorLockType.Missile, rule_func=can_morph_ball)
            },
        )
    }
