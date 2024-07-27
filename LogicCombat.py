
from enum import Enum

from BaseClasses import CollectionState
from .Items import SuitUpgrade
from .Logic import can_charge_beam, can_plasma_beam, can_power_beam, can_wave_beam, can_xray, has_energy_tanks
from .data.RoomNames import RoomName
import typing

if typing.TYPE_CHECKING:
    from .PrimeOptions import MetroidPrimeOptions


class CombatLogicDifficulty(Enum):
    NO_LOGIC = -1
    NORMAL = 0
    MINIMAL = 1


def _get_options(state: CollectionState, player: int) -> 'MetroidPrimeOptions':
    return state.multiworld.worlds[player].options


def _can_combat_generic(state: CollectionState, player: int, normal_tanks: int, minimal_tanks: int, requires_charge_beam: bool = True) -> bool:
    difficulty = _get_options(state, player).combat_logic_difficulty.value
    if difficulty == CombatLogicDifficulty.NO_LOGIC.value:
        return True
    elif difficulty == CombatLogicDifficulty.NORMAL.value:
        return has_energy_tanks(state, player, normal_tanks) and (can_charge_beam(state, player) or not requires_charge_beam)
    elif difficulty == CombatLogicDifficulty.MINIMAL.value:
        return has_energy_tanks(state, player, minimal_tanks) and (can_charge_beam(state, player) or not requires_charge_beam)


def can_combat_mines(state: CollectionState, player: int) -> bool:
    return _can_combat_generic(state, player, 5, 3)


def can_combat_labs(state: CollectionState, player: int) -> bool:
    return _get_options(state, player).starting_room_name.value in [RoomName.East_Tower.value, RoomName.Save_Station_B.value]
           or _can_combat_generic(state, player, 1, 0, False)


def can_combat_thardus(state: CollectionState, player: int) -> bool:
    """Require charge and plasma or power for thardus on normal"""
    if _get_options(state, player).starting_room_name.value in [RoomName.Quarantine_Monitor.value, RoomName.Save_Station_B.value]:
        return can_plasma_beam(state, player) or can_power_beam(state, player) or can_wave_beam(state, player)
    difficulty = _get_options(state, player).combat_logic_difficulty.value
    if difficulty == CombatLogicDifficulty.NO_LOGIC.value:
        return True
    elif difficulty == CombatLogicDifficulty.NORMAL.value:
        return has_energy_tanks(state, player, 3) and (can_charge_beam(state, player) and (can_plasma_beam(state, player) or can_power_beam(state, player)))
    elif difficulty == CombatLogicDifficulty.MINIMAL.value:
        return has_energy_tanks(state, player, 1) and can_plasma_beam(state, player) or can_power_beam(state, player) or can_wave_beam(state, player)


def can_combat_omega_pirate(state: CollectionState, player: int) -> bool:
    return _can_combat_generic(state, player, 6, 3)


def can_combat_flaaghra(state: CollectionState, player: int) -> bool:
    return _get_options(state, player).starting_room_name == RoomName.Sunchamber_Lobby.value
           or _can_combat_generic(state, player, 2, 1, False)


def can_combat_ridley(state: CollectionState, player: int) -> bool:
    return _can_combat_generic(state, player, 8, 8)


def can_combat_prime(state: CollectionState, player: int) -> bool:
    return _can_combat_generic(state, player, 8, 5)


def can_combat_ghosts(state: CollectionState, player: int) -> bool:
    difficulty = _get_options(state, player).combat_logic_difficulty.value
    if difficulty == CombatLogicDifficulty.NO_LOGIC.value:
        return True
    elif difficulty == CombatLogicDifficulty.NORMAL.value:
        return can_charge_beam(state, player, SuitUpgrade.Power_Beam) and can_power_beam(state, player) and can_xray(state, player, True)
    elif difficulty == CombatLogicDifficulty.MINIMAL.value:
        return can_charge_beam(state, player, SuitUpgrade.Power_Beam) and (can_power_beam(state, player) or can_xray(state, player, True))
