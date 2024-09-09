import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Callable, Dict, List, Optional

from ..DoorRando import BEAM_TO_LOCK_MAPPING

from ..LogicCombat import CombatLogicDifficulty

from ..Items import SuitUpgrade, get_item_for_options
from ..data.AreaNames import MetroidPrimeArea
from ..data.RoomNames import RoomName

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld

# TODO: Make starting_beam an attribute on the start room data instead of another regular item, update in init and tests
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

    no_power_beam_door_on_starting_level: Optional[bool] = False
    """Used when the starting beam is required to not be insta bk'd"""


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
        is_eligible=lambda world: world.options.disable_starting_room_bk_prevention.value != True,  # Varia suit is definitely required here
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
        no_power_beam_door_on_starting_level=True,
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
        ]
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


def _has_elevator_rando(world: 'MetroidPrimeWorld') -> bool:
    return world.options.elevator_randomization.value


def _has_no_pre_scan_elevators_with_shuffle_scan(world: 'MetroidPrimeWorld') -> bool:
    return world.options.pre_scan_elevators.value == False and world.options.shuffle_scan_visor.value


def _has_options_that_allow_more_landing_site_checks(world: 'MetroidPrimeWorld') -> bool:
    return world.options.blast_shield_randomization.value != 'None' or world.options.trick_difficulty.value != -1


def init_starting_room_data(world: 'MetroidPrimeWorld'):
    difficulty = world.options.starting_room.value
    yaml_name = world.options.starting_room_name.value
    world.prefilled_item_map = {}
    if yaml_name:
        if yaml_name in all_start_rooms:
            world.starting_room_data = get_starting_room_by_name(world, yaml_name)
        else:
            world.starting_room_data = StartRoomData(name=world.options.starting_room_name.value)
            world.starting_room_data.loadouts = [StartRoomLoadout(loadout=[SuitUpgrade.Power_Beam])]
    else:
        if world.options.starting_room.value == StartRoomDifficulty.Normal.value:
            if (_has_elevator_rando(world) or _has_no_pre_scan_elevators_with_shuffle_scan(world)) and not _has_options_that_allow_more_landing_site_checks(world):
                # Can't start at landing site since there are no pickups without tricks
                world.starting_room_data = get_starting_room_by_name(world, RoomName.Save_Station_1.value)

            else:
                world.starting_room_data = get_starting_room_by_name(world, RoomName.Landing_Site.value)
            # Give the randomizer more flexibility if they have options that allow more starting_room checks
            if _has_options_that_allow_more_landing_site_checks(world):
                world.options.disable_starting_room_bk_prevention.value = True
        else:
            world.starting_room_data = get_random_start_room_by_difficulty(world, difficulty)
        world.options.starting_room_name.value = world.starting_room_data.name


def init_starting_loadout(world: 'MetroidPrimeWorld'):
    disable_bk_prevention = world.options.disable_starting_room_bk_prevention.value
   # Clear non starting beam upgrades out of loadout
    if disable_bk_prevention:
        world.starting_room_data.selected_loadout.loadout = [item for item in world.starting_room_data.selected_loadout.loadout if item in BEAM_ITEMS]

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


# TODO: Make starting beam an explicit attribute on the start room data
def init_starting_beam(world: 'MetroidPrimeWorld'):
    loadout_beam = next((item for item in world.starting_room_data.selected_loadout.loadout if item in BEAM_ITEMS), None)

    def replace_starting_beam(new_beam: SuitUpgrade):
        if loadout_beam != None:
            world.starting_room_data.selected_loadout.loadout.remove(loadout_beam)
        world.starting_room_data.selected_loadout.loadout.append(new_beam)
        world.options.starting_beam.value = new_beam.value

    # Use the starting beam if it was set in the options (or for UT)
    if world.options.starting_beam.value is not None and world.options.starting_beam.value != "none":
        new_beam = SuitUpgrade.get_by_value(world.options.starting_beam)
        if new_beam != None:
            replace_starting_beam(new_beam)

    # Remap beam to a new color based on door randomization
    elif world.options.door_color_randomization != "none" and loadout_beam != None and loadout_beam != SuitUpgrade.Power_Beam and not world.starting_room_data.force_starting_beam:
        # replace the beam with whatever the new one should be mapped to
        original_door_color = BEAM_TO_LOCK_MAPPING[loadout_beam].value
        # Select new beam based off of what the original color is now mapped to
        new_beam = None
        for original, new in world.door_color_mapping[world.starting_room_data.area.value].type_mapping.items():
            if original == original_door_color:
                # Find the beam that corresponds to the new color
                for beam in BEAM_ITEMS:
                    if BEAM_TO_LOCK_MAPPING[beam].value == new:
                        new_beam = beam
                        break
                break
        replace_starting_beam(new_beam)

    # Randomize starting beam if enabled
    elif world.options.randomize_starting_beam and not world.starting_room_data.force_starting_beam:
        new_beam = world.random.choice([beam for beam in BEAM_ITEMS if beam != SuitUpgrade.Power_Beam])
        replace_starting_beam(new_beam)

    # Hive mecha needs to be disabled if we don't have power beam in vanilla start locations (otherwise no checks can be reached)
    # TODO: Make this use the new starting beam data
    if (world.starting_room_data.name == RoomName.Landing_Site.value or world.starting_room_data.name == RoomName.Save_Station_1.value) and SuitUpgrade.Power_Beam not in world.starting_room_data.selected_loadout.loadout:
        world.options.remove_hive_mecha.value = True
