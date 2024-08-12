import copy
from dataclasses import dataclass, field
from enum import Enum
import os
from typing import TYPE_CHECKING, Callable, Dict, List, Optional

from ..DoorRando import BEAM_TO_LOCK_MAPPING

from ..LogicCombat import CombatLogicDifficulty

from ..Items import SuitUpgrade, get_item_for_options
from ..data.AreaNames import MetroidPrimeArea
from ..data.RoomNames import RoomName

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld

BEAM_ITEMS = [SuitUpgrade.Power_Beam, SuitUpgrade.Ice_Beam, SuitUpgrade.Wave_Beam, SuitUpgrade.Plasma_Beam]


class StartRoomDifficulty(Enum):
    Normal = -1
    Safe = 0
    Dangerous = 1
    Buckle_Up = 2


@dataclass
class StartRoomLoadout:
    loadout: List[SuitUpgrade] = field(default_factory=list)
    item_rules: List[Dict[str, List[SuitUpgrade]]] = field(default_factory=list)
    """List of locations that can have a list of possible required items for that location"""


@dataclass
class StartRoomData:
    area: MetroidPrimeArea
    loadouts: List[StartRoomLoadout] = field(default_factory=list)
    difficulty: StartRoomDifficulty = StartRoomDifficulty.Safe
    selected_loadout: Optional[StartRoomLoadout] = None
    name: Optional[str] = None
    is_eligible: Callable[['MetroidPrimeWorld'], bool] = lambda world: True
    allowed_elevators: Optional[Dict[str, Dict[str, List[str]]]] = None
    denied_elevators: Optional[Dict[str, Dict[str, List[str]]]] = None
    force_starting_beam: Optional[bool] = False
    """Used for situations where starting beam cannot be randomized, disqualifies a room from being selected when randomizing blue doors is on"""


all_start_rooms: Dict[str, StartRoomData] = {
    RoomName.Landing_Site.value: StartRoomData(difficulty=StartRoomDifficulty.Normal, area=MetroidPrimeArea.Tallon_Overworld, loadouts=[StartRoomLoadout([SuitUpgrade.Power_Beam], [
        {"Chozo Ruins: Hive Totem": [SuitUpgrade.Missile_Launcher]}
    ])]),
    RoomName.Arboretum.value: StartRoomData(
        area=MetroidPrimeArea.Chozo_Ruins,
        loadouts=[StartRoomLoadout([SuitUpgrade.Missile_Launcher])],
    ),
    RoomName.Burn_Dome_Access.value: StartRoomData(
        area=MetroidPrimeArea.Chozo_Ruins,
        loadouts=[StartRoomLoadout([SuitUpgrade.Morph_Ball],
                                   item_rules=[
            {
                'Chozo Ruins: Burn Dome - Incinerator Drone': [SuitUpgrade.Morph_Ball_Bomb],
                'Chozo Ruins: Burn Dome - Missile': [SuitUpgrade.Missile_Launcher]
            }
        ]
        )],
        difficulty=StartRoomDifficulty.Safe,
    ),
    RoomName.Ruined_Fountain.value: StartRoomData(
        area=MetroidPrimeArea.Chozo_Ruins,
        loadouts=[StartRoomLoadout([SuitUpgrade.Missile_Launcher]),
                  StartRoomLoadout([SuitUpgrade.Morph_Ball])],
    ),
    RoomName.Save_Station_1.value: StartRoomData(
        area=MetroidPrimeArea.Chozo_Ruins,
        force_starting_beam=True,
        loadouts=[StartRoomLoadout([SuitUpgrade.Power_Beam],
                                   item_rules=[
            {"Chozo Ruins: Hive Totem": [SuitUpgrade.Missile_Launcher]}
        ])]),
    RoomName.Save_Station_2.value: StartRoomData(area=MetroidPrimeArea.Chozo_Ruins, loadouts=[StartRoomLoadout([SuitUpgrade.Missile_Launcher])]),
    RoomName.Tower_Chamber.value: StartRoomData(area=MetroidPrimeArea.Chozo_Ruins, loadouts=[StartRoomLoadout([SuitUpgrade.Wave_Beam],
                                                                                                              item_rules=[
        {
            "Chozo Ruins: Tower Chamber": [SuitUpgrade.Morph_Ball],
            "Chozo Ruins: Ruined Shrine - Plated Beetle": [SuitUpgrade.Morph_Ball_Bomb, SuitUpgrade.Main_Power_Bomb],
            "Chozo Ruins: Ruined Shrine - Lower Tunnel": [SuitUpgrade.Missile_Launcher],
        },
    ]
    )]),
    RoomName.Warrior_Shrine.value: StartRoomData(
        area=MetroidPrimeArea.Magmoor_Caverns,
        loadouts=[
            StartRoomLoadout([SuitUpgrade.Varia_Suit], [
                {
                    "Magmoor Caverns: Warrior Shrine": [SuitUpgrade.Morph_Ball],
                    "Magmoor Caverns: Storage Cavern": [SuitUpgrade.Morph_Ball_Bomb, SuitUpgrade.Main_Power_Bomb],
                }
            ]),
        ],
        allowed_elevators={
            MetroidPrimeArea.Magmoor_Caverns.value: {
                RoomName.Transport_to_Chozo_Ruins_North.value: [RoomName.Transport_to_Magmoor_Caverns_East.value, RoomName.Transport_to_Chozo_Ruins_West.value, RoomName.Transport_to_Tallon_Overworld_North.value]
            }
        }
    ),
    RoomName.East_Tower.value: StartRoomData(area=MetroidPrimeArea.Phendrana_Drifts, loadouts=[StartRoomLoadout([SuitUpgrade.Wave_Beam, SuitUpgrade.Missile_Launcher],
                                                                                                                [
        {
            "Phendrana Drifts: Phendrana Canyon": [SuitUpgrade.Space_Jump_Boots],
            "Phendrana Drifts: Research Lab Aether - Tank": [SuitUpgrade.Plasma_Beam]
        }
    ],
    )],
        is_eligible=lambda world: world.options.shuffle_scan_visor.value == False or world.multiworld.players > 1,
        difficulty=StartRoomDifficulty.Buckle_Up),

    RoomName.Save_Station_B.value: StartRoomData(
        area=MetroidPrimeArea.Phendrana_Drifts,
        force_starting_beam=True,
        loadouts=[
            StartRoomLoadout([SuitUpgrade.Plasma_Beam, SuitUpgrade.Missile_Launcher],
                             item_rules=[
                {"Phendrana Drifts: Phendrana Shorelines - Behind Ice": [SuitUpgrade.Space_Jump_Boots, SuitUpgrade.Morph_Ball]},
            ],
            )
        ], is_eligible=lambda world:
        world.options.combat_logic_difficulty.value == CombatLogicDifficulty.NO_LOGIC.value or world.options.elevator_randomization.value or world.multiworld.players > 1,
        denied_elevators={
            MetroidPrimeArea.Phendrana_Drifts.value: {
                RoomName.Transport_to_Magmoor_Caverns_West.value: [RoomName.Transport_to_Phazon_Mines_East.value, RoomName.Transport_to_Tallon_Overworld_East.value, "Chozo Ruins :" + RoomName.Transport_to_Tallon_Overworld_South.value, RoomName.Transport_to_Tallon_Overworld_West.value, RoomName.Transport_to_Phendrana_Drifts_South.value, RoomName.Transport_to_Phazon_Mines_West.value],
                "Phendrana Drifts: " + RoomName.Transport_to_Magmoor_Caverns_South.value: [RoomName.Transport_to_Chozo_Ruins_North.value]
            }
        }

    ),
    RoomName.Arbor_Chamber.value: StartRoomData(
        area=MetroidPrimeArea.Tallon_Overworld,
        loadouts=[StartRoomLoadout([SuitUpgrade.Missile_Launcher])],
        denied_elevators={
            MetroidPrimeArea.Tallon_Overworld.value: {
                RoomName.Transport_to_Chozo_Ruins_West.value: ["Phendrana Drifts: " + RoomName.Transport_to_Magmoor_Caverns_South.value, "Phazon Mines: " + RoomName.Transport_to_Magmoor_Caverns_South.value],
                RoomName.Transport_to_Magmoor_Caverns_East.value: ["Phendrana Drifts: " + RoomName.Transport_to_Magmoor_Caverns_South.value, "Phazon Mines: " + RoomName.Transport_to_Magmoor_Caverns_South.value],
            }
        }
    ),
    RoomName.Transport_to_Chozo_Ruins_East.value: StartRoomData(area=MetroidPrimeArea.Tallon_Overworld, loadouts=[StartRoomLoadout([SuitUpgrade.Ice_Beam, SuitUpgrade.Morph_Ball],
                                                                                                                                   item_rules=[
        {
            "Tallon Overworld: Overgrown Cavern": [SuitUpgrade.Missile_Launcher]
        }
    ]
    )]),
    RoomName.Quarantine_Monitor.value: StartRoomData(area=MetroidPrimeArea.Phendrana_Drifts, loadouts=[StartRoomLoadout([SuitUpgrade.Wave_Beam, SuitUpgrade.Thermal_Visor],
                                                                                                                        item_rules=[
        {
            "Phendrana Drifts: Quarantine Monitor": [SuitUpgrade.Morph_Ball],
            "Phendrana Drifts: Quarantine Cave": [SuitUpgrade.Spider_Ball],
            "Phendrana Drifts: Ice Ruins East - Spider Track": [SuitUpgrade.Space_Jump_Boots],
            "Phendrana Drifts: Ruined Courtyard": [SuitUpgrade.Plasma_Beam]
        },
    ]
    )], difficulty=StartRoomDifficulty.Buckle_Up,
        is_eligible=lambda world: world.options.shuffle_scan_visor.value == False or world.multiworld.players > 1,
    ),
    RoomName.Sunchamber_Lobby.value: StartRoomData(
        area=MetroidPrimeArea.Chozo_Ruins,
        loadouts=[
            StartRoomLoadout([SuitUpgrade.Morph_Ball, SuitUpgrade.Missile_Launcher, SuitUpgrade.Morph_Ball_Bomb]),
            StartRoomLoadout([SuitUpgrade.Morph_Ball, SuitUpgrade.Missile_Launcher, SuitUpgrade.Main_Power_Bomb])
        ],
        difficulty=StartRoomDifficulty.Buckle_Up
    ),

}


def get_random_start_room_by_difficulty(world: 'MetroidPrimeWorld', difficulty: int) -> StartRoomData:
    """Returns a random start room based on difficulty as well as a random loadout from that room"""
    available_room_names = [name for name, room in all_start_rooms.items() if room.difficulty.value == difficulty and room.is_eligible(world)]
    room_name = world.random.choice(available_room_names)
    return get_starting_room_by_name(world, room_name)


def get_starting_room_by_name(world: 'MetroidPrimeWorld', room_name: str) -> StartRoomData:
    """Returns a start room based on name"""
    # Prevent us from modifying the original room data
    room = copy.deepcopy(all_start_rooms[room_name])
    room.name = room_name
    if len(room.loadouts) == 0:
        room.selected_loadout = StartRoomLoadout([SuitUpgrade.Power_Beam])
    else:
        room.selected_loadout = world.random.choice(room.loadouts)
    return room


def _is_elevator_rando_with_vanilla_starting_room(world: 'MetroidPrimeWorld') -> bool:
    return world.options.elevator_randomization.value and world.options.starting_room.value == StartRoomDifficulty.Normal.value


def _is_no_pre_scan_elevators_with_shuffle_scan_and_vanilla_starting_room(world: 'MetroidPrimeWorld') -> bool:
    return world.options.pre_scan_elevators.value == False and world.options.shuffle_scan_visor.value and world.options.starting_room.value == StartRoomDifficulty.Normal.value


def init_starting_room_data(world: 'MetroidPrimeWorld'):
    difficulty = world.options.starting_room.value
    yaml_name = world.options.starting_room_name.value
    disable_bk_prevention = world.options.disable_starting_room_bk_prevention.value

    world.prefilled_item_map = {}
    if yaml_name:
        if yaml_name in all_start_rooms:
            world.starting_room_data = get_starting_room_by_name(world, yaml_name)
        else:
            world.starting_room_data = StartRoomData(name=world.options.starting_room_name.value)
            world.starting_room_data.loadouts = [StartRoomLoadout(loadout=[SuitUpgrade.Power_Beam])]
    else:
        if _is_elevator_rando_with_vanilla_starting_room(world) or _is_no_pre_scan_elevators_with_shuffle_scan_and_vanilla_starting_room(world):
            # Can't start at landing site since there are no pickups without tricks
            world.starting_room_data = get_starting_room_by_name(world, RoomName.Save_Station_1.value)
        else:
            world.starting_room_data = get_random_start_room_by_difficulty(world, difficulty)
        world.options.starting_room_name.value = world.starting_room_data.name

    # Clear non starting beam upgrades out of loadout
    if disable_bk_prevention:
        world.starting_room_data.selected_loadout.loadout = [item for item in world.starting_room_data.selected_loadout.loadout if item in BEAM_ITEMS]

    loadout_beam = next((item for item in world.starting_room_data.selected_loadout.loadout if item in BEAM_ITEMS), None)
    if world.options.door_color_randomization != "none" and loadout_beam is not None and loadout_beam is not SuitUpgrade.Power_Beam and not world.starting_room_data.force_starting_beam:
        # replace the beam with a random one
        world.starting_room_data.selected_loadout.loadout.remove(loadout_beam)
        original_door_color = BEAM_TO_LOCK_MAPPING[loadout_beam].value
        # Select new beam based off of what the original color is now mapped to
        new_beam = None
        for original, new in world.options.door_color_mapping[world.starting_room_data.area.value].type_mapping.items():
            if original == original_door_color:
                # Find the beam that corresponds to the new color
                for beam in BEAM_ITEMS:
                    if BEAM_TO_LOCK_MAPPING[beam].value == new:
                        new_beam = beam
                        break
                break

        world.starting_room_data.selected_loadout.loadout.append(new_beam)

        # Update the loadout with the correct items based on options (progressive upgrades, missile launcher, etc.)
    updated_loadout = []
    for item in world.starting_room_data.selected_loadout.loadout:
        updated_loadout.append(get_item_for_options(world, item))
    world.starting_room_data.selected_loadout.loadout = updated_loadout

    # If we aren't preventing bk then set a few items for prefill if available
    if not disable_bk_prevention:
        for mapping in world.starting_room_data.selected_loadout.item_rules:
            for location_name, potential_items in mapping.items():
                required_item = get_item_for_options(world, world.random.choice(potential_items))
                world.prefilled_item_map[location_name] = required_item.value
