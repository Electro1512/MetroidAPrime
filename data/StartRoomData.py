from dataclasses import dataclass, field
from enum import Enum
import random
from typing import TYPE_CHECKING, Callable, Dict, List, Optional
from worlds.metroidprime.Items import MetroidPrimeItem, SuitUpgrade
from worlds.metroidprime.data.RoomNames import RoomName

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


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
    loadouts: List[StartRoomLoadout] = field(default_factory=list)
    difficulty: StartRoomDifficulty = StartRoomDifficulty.Safe
    selected_loadout: Optional[StartRoomLoadout] = None
    name: Optional[str] = None


all_start_rooms: Dict[str, StartRoomData] = {
    RoomName.Landing_Site.value: StartRoomData(difficulty=StartRoomDifficulty.Normal),
    RoomName.Arboretum.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Missile_Launcher])]),
    RoomName.Burn_Dome_Access.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Morph_Ball])], StartRoomDifficulty.Dangerous),
    RoomName.Ruined_Fountain.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Missile_Launcher]), StartRoomLoadout([SuitUpgrade.Morph_Ball])]),
    RoomName.Save_Station_1.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Power_Beam])]),
    RoomName.Save_Station_2.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Missile_Launcher])]),
    RoomName.Tower_Chamber.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Wave_Beam])]),
    RoomName.Warrior_Shrine.value: StartRoomData([
        StartRoomLoadout([SuitUpgrade.Wave_Beam, SuitUpgrade.Varia_Suit]),
        StartRoomLoadout([SuitUpgrade.Plasma_Beam, SuitUpgrade.Varia_Suit])
    ], StartRoomDifficulty.Dangerous),
    # Start here for figuring out rest
    RoomName.Transport_to_Magmoor_Caverns_North.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Morph_Ball])]),
    RoomName.Aether_Lab_Entryway.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Wave_Beam, SuitUpgrade.Missile_Launcher])]),
    RoomName.Chozo_Ice_Temple.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Plasma_Beam, SuitUpgrade.Missile_Launcher])]),
    RoomName.Control_Tower.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Wave_Beam, SuitUpgrade.Missile_Launcher])]),
    RoomName.Ice_Ruins_East.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Plasma_Beam])]),
    RoomName.Ice_Ruins_West.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Plasma_Beam])]),
    RoomName.Phendrana_Canyon.value: StartRoomData([
        StartRoomLoadout([SuitUpgrade.Plasma_Beam, SuitUpgrade.Space_Jump_Boots]),
        StartRoomLoadout([SuitUpgrade.Plasma_Beam, SuitUpgrade.Missile_Launcher])
    ]),

    RoomName.Research_Lab_Hydra.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Plasma_Beam, SuitUpgrade.Wave_Beam])]),
    RoomName.Ruined_Courtyard.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Plasma_Beam])]),
    RoomName.Save_Station_B.value: StartRoomData([
        StartRoomLoadout([SuitUpgrade.Plasma_Beam, SuitUpgrade.Missile_Launcher],
                         item_rules=[
            {"Phendrana Drifts: Phendrana Shorelines - Behind Ice": [SuitUpgrade.Space_Jump_Boots, SuitUpgrade.Morph_Ball]
             },
        ]
        )
    ]),
    RoomName.Save_Station_D.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Wave_Beam, SuitUpgrade.Missile_Launcher])]),
    RoomName.Transport_to_Magmoor_Caverns_West.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Plasma_Beam, SuitUpgrade.Missile_Launcher])]),
    RoomName.Arbor_Chamber.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Missile_Launcher])]),
    RoomName.Transport_to_Chozo_Ruins_East.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Ice_Beam, SuitUpgrade.Morph_Ball])])
}


def get_random_start_room_by_difficulty(difficulty: int) -> StartRoomData:
    """Returns a random start room based on difficulty as well as a random loadout from that room"""
    available_room_names = [name for name, room in all_start_rooms.items() if room.difficulty.value == difficulty]
    room_name = random.choice(available_room_names)
    return get_starting_room_by_name(room_name)


def get_starting_room_by_name(room_name: str) -> StartRoomData:
    """Returns a start room based on name"""
    room = all_start_rooms[room_name]
    room.name = room_name
    if len(room.loadouts) == 0:
        room.selected_loadout = StartRoomLoadout([SuitUpgrade.Power_Beam])
    else:
        room.selected_loadout = random.choice(room.loadouts)
    return room


def init_starting_room_data(world: 'MetroidPrimeWorld'):
    difficulty = world.options.starting_room.value
    yaml_name = world.options.starting_room_name.value
    if yaml_name:
        if yaml_name in all_start_rooms:
            world.starting_room_data = get_starting_room_by_name(yaml_name)
        else:
            world.starting_room_data = StartRoomData(name=world.options.starting_room_name.value)
            world.starting_room_data.loadouts = [StartRoomLoadout(loadout=[SuitUpgrade.Power_Beam])]
    else:
        world.starting_room_data = get_random_start_room_by_difficulty(difficulty)
        world.options.starting_room_name.value = world.starting_room_data.name

    if not world.options.missile_launcher.value and SuitUpgrade.Missile_Launcher.value in world.starting_room_data.selected_loadout.loadout:
        # Change starting loadout missile launcher to be missile expansion
        world.starting_room_data.selected_loadout.loadout.remove(SuitUpgrade.Missile_Launcher.value)
        world.starting_room_data.selected_loadout.loadout.append(SuitUpgrade.Missile_Expansion.value)

    for mapping in world.starting_room_data.selected_loadout.item_rules:
        for location_name, potential_items in mapping.items():
            required_item = random.choice(potential_items)
            world.prefilled_item_map[location_name] = required_item.value
