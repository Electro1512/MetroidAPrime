import copy
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
    RoomName.Landing_Site.value: StartRoomData(difficulty=StartRoomDifficulty.Normal, loadouts=[StartRoomLoadout([SuitUpgrade.Power_Beam], [
        {"Chozo Ruins: Hive Totem": [SuitUpgrade.Missile_Launcher]}
    ])]),
    RoomName.Arboretum.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Missile_Launcher])]),
    RoomName.Burn_Dome_Access.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Morph_Ball],
                                                                     item_rules=[
        {
            'Chozo Ruins: Burn Dome - Incinerator Drone': [SuitUpgrade.Morph_Ball_Bomb],
            'Chozo Ruins: Burn Dome - Missile': [SuitUpgrade.Missile_Launcher]
        }
    ]
    )], StartRoomDifficulty.Safe),
    RoomName.Ruined_Fountain.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Missile_Launcher]), StartRoomLoadout([SuitUpgrade.Morph_Ball])]),
    RoomName.Save_Station_1.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Power_Beam],
                                                                   item_rules=[
        {"Chozo Ruins: Hive Totem": [SuitUpgrade.Missile_Launcher]}
    ])]),
    RoomName.Save_Station_2.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Missile_Launcher])]),
    RoomName.Tower_Chamber.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Wave_Beam],
                                                                  item_rules=[
        {
            "Chozo Ruins: Tower Chamber": [SuitUpgrade.Morph_Ball],
            "Chozo Ruins: Ruined Shrine - Plated Beetle": [SuitUpgrade.Morph_Ball_Bomb],
            "Chozo Ruins: Ruined Shrine - Lower Tunnel": [SuitUpgrade.Missile_Launcher],
        },
    ]
    )]),
    RoomName.Warrior_Shrine.value: StartRoomData([
        StartRoomLoadout([SuitUpgrade.Varia_Suit], [
            {
                "Magmoor Caverns: Warrior Shrine": [SuitUpgrade.Morph_Ball],
                "Magmoor Caverns: Storage Cavern": [SuitUpgrade.Morph_Ball_Bomb, SuitUpgrade.Main_Power_Bomb],
            }
        ]),
    ], StartRoomDifficulty.Safe),
    RoomName.East_Tower.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Wave_Beam, SuitUpgrade.Missile_Launcher],
                                                               [
        {
            "Phendrana Drifts: Phendrana Canyon": [SuitUpgrade.Space_Jump_Boots],
            "Phendrana Drifts: Research Lab Aether - Tank": [SuitUpgrade.Plasma_Beam]
        }
    ]
    )], StartRoomDifficulty.Buckle_Up),

    RoomName.Save_Station_B.value: StartRoomData([
        StartRoomLoadout([SuitUpgrade.Plasma_Beam, SuitUpgrade.Missile_Launcher],
                         item_rules=[
            {"Phendrana Drifts: Phendrana Shorelines - Behind Ice": [SuitUpgrade.Space_Jump_Boots, SuitUpgrade.Morph_Ball]},
        ]
        )
    ]),
    RoomName.Arbor_Chamber.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Missile_Launcher])]),
    RoomName.Transport_to_Chozo_Ruins_East.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Ice_Beam, SuitUpgrade.Morph_Ball],
                                                                                  item_rules=[
        {
            "Tallon Overworld: Overgrown Cavern": [SuitUpgrade.Missile_Launcher]
        }
    ]
    )]),
    RoomName.Quarantine_Monitor.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Wave_Beam, SuitUpgrade.Morph_Ball],
                                                                       item_rules=[
        {
            "Phendrana Drifts: Quarantine Monitor": [SuitUpgrade.Thermal_Visor],
            "Phendrana Drifts: Quarantine Cave": [SuitUpgrade.Spider_Ball],
            "Phendrana Drifts: Ice Ruins East - Spider Track": [SuitUpgrade.Space_Jump_Boots],
            "Phendrana Drifts: Ruined Courtyard": [SuitUpgrade.Plasma_Beam]
        },
    ]
    )], StartRoomDifficulty.Buckle_Up
    ),
    RoomName.Sunchamber_Lobby.value: StartRoomData([StartRoomLoadout([SuitUpgrade.Morph_Ball, SuitUpgrade.Missile_Launcher, SuitUpgrade.Morph_Ball_Bomb])], StartRoomDifficulty.Buckle_Up),

}


def get_random_start_room_by_difficulty(difficulty: int) -> StartRoomData:
    """Returns a random start room based on difficulty as well as a random loadout from that room"""
    available_room_names = [name for name, room in all_start_rooms.items() if room.difficulty.value == difficulty]
    room_name = random.choice(available_room_names)
    return get_starting_room_by_name(room_name)


def get_starting_room_by_name(room_name: str) -> StartRoomData:
    """Returns a start room based on name"""
    # Prevent us from modifying the original room data
    room = copy.deepcopy(all_start_rooms[room_name])
    room.name = room_name
    if len(room.loadouts) == 0:
        room.selected_loadout = StartRoomLoadout([SuitUpgrade.Power_Beam])
    else:
        room.selected_loadout = random.choice(room.loadouts)
    return room


def _get_missile_item(world: 'MetroidPrimeWorld') -> SuitUpgrade:
    if world.options.missile_launcher.value:
        return SuitUpgrade.Missile_Launcher
    return SuitUpgrade.Missile_Expansion


def _get_power_bomb_item(world: 'MetroidPrimeWorld') -> SuitUpgrade:
    if world.options.main_power_bomb.value:
        return SuitUpgrade.Main_Power_Bomb
    return SuitUpgrade.Power_Bomb_Expansion


def _get_item_for_options(world: 'MetroidPrimeWorld', item: SuitUpgrade) -> SuitUpgrade:
    if item == SuitUpgrade.Missile_Launcher:
        return _get_missile_item(world)
    if item == SuitUpgrade.Main_Power_Bomb:
        return _get_power_bomb_item(world)
    return item


def init_starting_room_data(world: 'MetroidPrimeWorld'):
    difficulty = world.options.starting_room.value
    yaml_name = world.options.starting_room_name.value
    world.prefilled_item_map = {}
    if yaml_name:
        if yaml_name in all_start_rooms:
            world.starting_room_data = get_starting_room_by_name(yaml_name)
        else:
            world.starting_room_data = StartRoomData(name=world.options.starting_room_name.value)
            world.starting_room_data.loadouts = [StartRoomLoadout(loadout=[SuitUpgrade.Power_Beam])]
    else:
        world.starting_room_data = get_random_start_room_by_difficulty(difficulty)
        world.options.starting_room_name.value = world.starting_room_data.name

    if SuitUpgrade.Missile_Launcher in world.starting_room_data.selected_loadout.loadout:
        # Change starting loadout missile launcher to be missile expansion
        world.starting_room_data.selected_loadout.loadout.remove(SuitUpgrade.Missile_Launcher)
        world.starting_room_data.selected_loadout.loadout.append(_get_missile_item(world))

    if SuitUpgrade.Main_Power_Bomb in world.starting_room_data.selected_loadout.loadout:
        # Update main power bomb
        world.starting_room_data.selected_loadout.loadout.remove(SuitUpgrade.Main_Power_Bomb)
        world.starting_room_data.selected_loadout.loadout.append(_get_power_bomb_item(world))

    for mapping in world.starting_room_data.selected_loadout.item_rules:
        for location_name, potential_items in mapping.items():
            required_item = _get_item_for_options(world, random.choice(potential_items))
            world.prefilled_item_map[location_name] = required_item.value
