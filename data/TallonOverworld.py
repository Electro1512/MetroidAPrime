
from worlds.metroidprime.data.Tricks import Trick, TrickDifficulty
from .RoomData import AreaData, Capabilities, DoorData, DoorLockType, MetroidPrimeArea, PickupData, RoomData, TrickData
from .RoomNames import RoomName


class TallonOverworldAreaData(AreaData):
    rooms = {

        RoomName.Alcove: RoomData(
            doors={
                0: DoorData(RoomName.Landing_Site, required_items=[Capabilities.Can_Space_Jump], tricks=[TrickData(Trick.Slope_Jump, 'Alcove Slope Jump Escape', TrickDifficulty.Medium)]),
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
                0: DoorData(RoomName.Cargo_Freight_Lift_to_Deck_Gamma, required_items=[Capabilities.Can_Move_Underwater, Capabilities.Can_Space_Jump]),
                1: DoorData(RoomName.Hydro_Access_Tunnel, required_items=[Capabilities.Can_Move_Underwater, Capabilities.Can_Thermal, Capabilities.Can_Wave_Beam, Capabilities.Can_Space_Jump])
            },
            pickups=[
                PickupData('Tallon Overworld: Biohazard Containment', required_items=[Capabilities.Can_Super_Missile]),
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
                0: DoorData(RoomName.Frigate_Crash_Site, defaultLock=DoorLockType.Ice, required_items=[Capabilities.Can_Morph_Ball, Capabilities.Can_Space_Jump], tricks=[TrickData(Trick.Slope_Jump_With_Space_Jump, 'Backwards Frigate Without Gravity', TrickDifficulty.Easy, additional_required_items=[Capabilities.Can_Morph_Ball])]),
                1: DoorData(RoomName.Biohazard_Containment,
                            required_items=[
                                Capabilities.Can_Morph_Ball,
                                Capabilities.Can_Move_Underwater,
                                Capabilities.Can_Space_Jump,
                                Capabilities.Can_Thermal,
                                Capabilities.Can_Wave_Beam
                            ],
                            tricks=[
                                TrickData(Trick.Slope_Jump_With_Space_Jump, 'Frigate without gravity suit', TrickDifficulty.Easy, additional_required_items=[Capabilities.Can_Morph_Ball, Capabilities.Can_Thermal, Capabilities.Can_Wave_Beam]),
                            ]
                            ),
            },
            pickups=[
                PickupData('Tallon Overworld: Cargo Freight Lift to Deck Gamma', required_items=[[Capabilities.Can_Missile], [Capabilities.Can_Charge_Beam]]),
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
                0: DoorData(RoomName.Waterfall_Cavern),
                1: DoorData(RoomName.Cargo_Freight_Lift_to_Deck_Gamma, defaultLock=DoorLockType.Ice,
                            # Items required for this one also include all the items required to get to the frieght lift inside the crashed frigate
                            required_items=[
                                Capabilities.Can_Space_Jump,
                                Capabilities.Can_Move_Underwater,
                                Capabilities.Can_Morph_Ball,
                                Capabilities.Can_Wave_Beam,
                                Capabilities.Can_Thermal
                            ],
                            tricks=[
                                TrickData(Trick.Slope_Jump_With_Space_Jump, 'Frigate Crash Site Slope Jump Without SpaceJump or Gravity', TrickDifficulty.Easy,
                                          additional_required_items=[
                                              Capabilities.Can_Morph_Ball,
                                              Capabilities.Can_Wave_Beam,
                                              Capabilities.Can_Thermal
                                          ]),
                            ]
                            ),
                2: DoorData(RoomName.Overgrown_Cavern, defaultLock=DoorLockType.Ice,
                            required_items=[Capabilities.Cannot_Reach],
                            tricks=[TrickData(Trick.Scan_Dash, 'Climb to Overgrown Cavern', TrickDifficulty.Hard, additional_required_items=[Capabilities.Can_Space_Jump, Capabilities.Can_Morph_Ball])]
                            ),
            },
            pickups=[
                PickupData('Tallon Overworld: Frigate Crash Site',
                           required_items=[Capabilities.Can_Space_Jump, Capabilities.Can_Move_Underwater],
                           tricks=[
                               TrickData(Trick.Scan_Dash, 'Frigate Crash Site Scan Dash', TrickDifficulty.Hard),
                               TrickData(Trick.Slope_Jump_With_Space_Jump, 'Frigate Crash Site Slope Jump', TrickDifficulty.Easy),
                               TrickData(Trick.Slope_Jump, 'Frigate Crash Site Slope Jump', TrickDifficulty.Hard),
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
                0: DoorData(RoomName.Hydro_Access_Tunnel, required_items=[Capabilities.Cannot_Reach], tricks=[TrickData(Trick.Double_Bomb_Jump, "Great Tree Hall Bars Skip", difficulty=TrickDifficulty.Hard)]),  # Can't reach from other doors unless you use a trick until after you go through frigate
                1: DoorData(RoomName.Great_Tree_Chamber, required_items=[Capabilities.Can_XRay, Capabilities.Can_Space_Jump], tricks=[TrickData(Trick.No_XRay, "Great Tree Hall XRay Skip", difficulty=TrickDifficulty.Easy)]),
                2: DoorData(RoomName.Transport_Tunnel_D, defaultLock=DoorLockType.Ice),  # Can't reach from other doors unless you use a trick until after you go through frigate
                3: DoorData(RoomName.Life_Grove_Tunnel, defaultLock=DoorLockType.Ice,
                            required_items=[Capabilities.Can_Spider],
                            tricks=[TrickData(Trick.L_Jump_Space_Jump, "Great Tree Hall Spider Ball Skip", difficulty=TrickDifficulty.Medium)]
                            ),
                4: DoorData(RoomName.Transport_Tunnel_E, defaultLock=DoorLockType.Ice, required_items=[Capabilities.Cannot_Reach], tricks=[TrickData(Trick.Double_Bomb_Jump, "Great Tree Hall Bars Skip", difficulty=TrickDifficulty.Hard, additional_required_items=[Capabilities.Can_Space_Jump])]),  # Can't reach from other doors unless you use a trick until after you go through frigate
            },
        ),

        RoomName.Gully: RoomData(
            doors={
                0: DoorData(RoomName.Tallon_Canyon, defaultLock=DoorLockType.Bomb, exclude_from_rando=True, required_items=[Capabilities.Can_Bomb, Capabilities.Can_Space_Jump]),
                1: DoorData(RoomName.Alcove, exclude_from_rando=True)  # Alcove Via Landing Site
            },
        ),

        RoomName.Hydro_Access_Tunnel: RoomData(
            doors={
                0: RoomData(RoomName.Great_Tree_Hall, required_items=[Capabilities.Can_Bomb, Capabilities.Can_Move_Underwater, Capabilities.Can_Boost]),  # Boost is needed to open way in great tree hall
                1: RoomData(RoomName.Biohazard_Containment, required_items=[Capabilities.Can_Bomb, Capabilities.Can_Move_Underwater],
                            tricks=[
                    TrickData(Trick.Slope_Jump_With_Space_Jump, 'Frigate without gravity suit', TrickDifficulty.Easy, additional_required_items=[Capabilities.Can_Morph_Ball, Capabilities.Can_Thermal, Capabilities.Can_Wave_Beam])]),
                # This one isn't an actual door but is instead accounting for not being able to access the great tree hall lower from upper
                2: DoorData(RoomName.Transport_Tunnel_E, destinationArea=MetroidPrimeArea.Tallon_Overworld, defaultLock=DoorLockType.Ice, required_items=[Capabilities.Can_Space_Jump], exclude_from_rando=True),
            },
            pickups=[
                PickupData('Tallon Overworld: Hydro Access Tunnel', required_items=[Capabilities.Can_Bomb, Capabilities.Can_Move_Underwater]),
            ]),

        RoomName.Landing_Site: RoomData(
            doors={
                0: DoorData(RoomName.Gully, required_items=[[Capabilities.Can_Space_Jump], [Capabilities.Can_Bomb, Capabilities.Can_Boost]], tricks=[TrickData(Trick.Scan_Dash, 'Landing Site Scan Dash', TrickDifficulty.Easy)]),
                1: DoorData(RoomName.Canyon_Cavern),
                2: DoorData(RoomName.Temple_Hall),
                3: DoorData(RoomName.Alcove, required_items=[[Capabilities.Can_Space_Jump], [Capabilities.Can_Bomb, Capabilities.Can_Boost]], tricks=[TrickData(Trick.Scan_Dash, 'Landing Site Scan Dash', TrickDifficulty.Easy)]),
                4: DoorData(RoomName.Waterfall_Cavern),
            },
            pickups=[
                PickupData('Tallon Overworld: Landing Site', required_items=[Capabilities.Can_Morph_Ball], tricks=[]),
            ]),

        RoomName.Life_Grove_Tunnel: RoomData(
            doors={
                0: DoorData(RoomName.Great_Tree_Hall, defaultLock=DoorLockType.Ice, required_items=[Capabilities.Can_Power_Bomb, Capabilities.Can_Boost], exclude_from_rando=True),
                1: DoorData(RoomName.Life_Grove, defaultLock=DoorLockType.None_, required_items=[Capabilities.Can_Power_Bomb, Capabilities.Can_Boost], exclude_from_rando=True)
            },
            pickups=[
                PickupData('Tallon Overworld: Life Grove Tunnel', required_items=[Capabilities.Can_Bomb, Capabilities.Can_Boost]),
            ]),

        RoomName.Life_Grove: RoomData(
            doors={DoorData(RoomName.Life_Grove_Tunnel, defaultLock=DoorLockType.None_,
                            required_items=[Capabilities.Can_Power_Bomb, Capabilities.Can_Space_Jump, Capabilities.Can_XRay, Capabilities.Can_Boost],
                            tricks=[TrickData()],
                            exclude_from_rando=True)},
            pickups=[
                PickupData('Tallon Overworld: Life Grove - Start'), PickupData('Tallon Overworld: Life Grove - Underwater Spinner', required_items=[Capabilities.Can_Boost, Capabilities.Can_Bomb]),
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
                0: DoorData(RoomName.Frigate_Crash_Site, defaultLock=DoorLockType.Ice, required_items=[Capabilities.Can_Morph_Ball]),
                1: DoorData(RoomName.Transport_Tunnel_C, destinationArea=MetroidPrimeArea.Tallon_Overworld, defaultLock=DoorLockType.Ice, required_items=[Capabilities.Can_Morph_Ball]),
            },
            pickups=[
                PickupData('Tallon Overworld: Overgrown Cavern', required_items=[Capabilities.Can_Morph_Ball]),
            ]),

        # RoomName.Reactor_Access: RoomData(
        # ),

        RoomName.Root_Cave: RoomData(
            doors={
                0: DoorData(RoomName.Transport_Tunnel_B, destinationArea=MetroidPrimeArea.Tallon_Overworld),
                1: DoorData(RoomName.Root_Tunnel),
                2: DoorData(RoomName.Arbor_Chamber, defaultLock=DoorLockType.Plasma,
                            required_items=[Capabilities.Can_Grapple, Capabilities.Can_XRay],
                            tricks=[TrickData(Trick.Combat_Dash_Space_Jump, 'Root Cave No Grapple', TrickDifficulty.Hard)]
                            ),

            },
            pickups=[
                PickupData('Tallon Overworld: Root Cave', ),
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
                2: DoorData(RoomName.Gully, defaultLock=DoorLockType.Bomb, required_items=[[Capabilities.Can_Space_Jump], [Capabilities.Can_Boost, Capabilities.Can_Bomb]]),
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
                0: RoomData(RoomName.Transport_Tunnel_D, defaultLock=DoorLockType.Ice),
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
                0: RoomData(RoomName.Transport_Tunnel_E, defaultLock=DoorLockType.Ice),
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
                0: RoomData(RoomName.Transport_to_Phazon_Mines_East, defaultLock=DoorLockType.Ice),
                1: RoomData(RoomName.Great_Tree_Hall, defaultLock=DoorLockType.Ice),
            },
        ),

        RoomName.Waterfall_Cavern: RoomData(
            doors={
                0: DoorData(RoomName.Landing_Site, required_items=[Capabilities.Can_Morph_Ball]),
                1: DoorData(RoomName.Tallon_Canyon, defaultLock=DoorLockType.Missile, required_items=[Capabilities.Can_Morph_Ball])
            },
        )
    }
