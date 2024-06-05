from BaseClasses import CollectionState
from worlds.metroidprime.PrimeOptions import MetroidPrimeOptions
from .Items import SuitUpgrade


def _get_options(state: CollectionState, player: int) -> MetroidPrimeOptions:
    return state.multiworld.worlds[player].options


def can_boost(state: CollectionState, player: int) -> bool:
    state.has_all([SuitUpgrade.Morph_Ball, SuitUpgrade.Boost_Ball], player)


def can_bomb(state: CollectionState, player: int) -> bool:
    state.has_all([SuitUpgrade.Morph_Ball, SuitUpgrade.Morph_Ball_Bomb], player)


def can_power_bomb(state: CollectionState, player: int) -> bool:
    if _get_options(state, player).main_power_bomb.value:
        return state.has_all([SuitUpgrade.Morph_Ball, SuitUpgrade.Main_Power_Bomb], player),

    return state.has_all([SuitUpgrade.Power_Bomb_Expansion, SuitUpgrade.Morph_Ball], player)


def can_spider(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Spider_Ball, SuitUpgrade.Morph_Ball], player)


def can_missile(state: CollectionState, player: int) -> bool:
    if _get_options(state, player).missile_launcher.value:
        return state.has(SuitUpgrade.Missile_Launcher, player)
    return state.has(SuitUpgrade.Missile_Expansion, player)


def can_super_missile(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Charge_Beam, SuitUpgrade.Super_Missile], player)


def can_wave_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Wave_Beam, player)


def can_ice_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Ice_Beam, player)


def can_plasma_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Plasma_Beam_Beam, player)


def can_melt_ice(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Plasma_Beam, player)


def can_grapple(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Grapple_Beam, player)


def can_space_jump(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Space_Jump_Boots, player)


def can_morph_ball(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Morph_Ball, player)


def can_xray(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.X_Ray_Visor, player)


def can_thermal(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Thermal_Visor, player)


def can_move_underwater(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Gravity_Suit, player)


def can_charge_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Charge_Beam, player)


def can_scan(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Scan_Visor, player)


def can_crashed_frigate(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball, SuitUpgrade.Space_Jump_Boots, SuitUpgrade.Wave_Beam, SuitUpgrade.Gravity_Suit, SuitUpgrade.Thermal_Visor], player)
