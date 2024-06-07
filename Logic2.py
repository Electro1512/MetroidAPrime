from BaseClasses import CollectionState
from worlds.metroidprime.PrimeOptions import MetroidPrimeOptions
from worlds.metroidprime.data.RoomNames import RoomName
from .Items import SuitUpgrade


def _get_options(state: CollectionState, player: int) -> MetroidPrimeOptions:
    return state.multiworld.worlds[player].options


def can_boost(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Boost_Ball.value], player)


def can_bomb(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Morph_Ball_Bomb.value], player)


def can_power_bomb(state: CollectionState, player: int) -> bool:
    if _get_options(state, player).main_power_bomb.value:
        return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Main_Power_Bomb.value], player),

    return state.has_all([SuitUpgrade.Power_Bomb_Expansion.value, SuitUpgrade.Morph_Ball.value], player)


def can_spider(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Spider_Ball.value, SuitUpgrade.Morph_Ball.value], player)


def can_missile(state: CollectionState, player: int) -> bool:
    if _get_options(state, player).missile_launcher.value:
        return state.has(SuitUpgrade.Missile_Launcher.value, player)
    return state.has(SuitUpgrade.Missile_Expansion.value, player)


def can_super_missile(state: CollectionState, player: int) -> bool:
    return can_missile(state, player) and state.has_all([SuitUpgrade.Charge_Beam.value, SuitUpgrade.Super_Missile.value], player)


def can_wave_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Wave_Beam.value, player)


def can_ice_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Ice_Beam.value, player)


def can_plasma_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Plasma_Beam.value, player)


def can_melt_ice(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Plasma_Beam.value, player)


def can_grapple(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Grapple_Beam.value, player)


def can_space_jump(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Space_Jump_Boots.value, player)


def can_morph_ball(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Morph_Ball.value, player)


def can_xray(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.X_Ray_Visor.value, player)


def can_thermal(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Thermal_Visor.value, player)


def can_move_underwater(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Gravity_Suit.value, player)


def can_charge_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Charge_Beam.value, player)


def can_scan(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Scan_Visor.value, player)


def can_crashed_frigate(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Space_Jump_Boots.value, SuitUpgrade.Wave_Beam.value, SuitUpgrade.Gravity_Suit.value, SuitUpgrade.Thermal_Visor.value, SuitUpgrade.Morph_Ball_Bomb], player)


def can_crashed_frigate_backwards(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Space_Jump_Boots.value, SuitUpgrade.Gravity_Suit.value, SuitUpgrade.Morph_Ball_Bomb], player)


def can_heat(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Varia_Suit.value, player)


def can_infinite_speed(state: CollectionState, player: int) -> bool:
    return can_boost(state, player) and can_bomb(state, player)


def can_exit_ruined_shrine(state: CollectionState, player: int) -> bool:
    return can_morph_ball(state, player) or can_space_jump(state, player)


def can_flaahgra(state: CollectionState, player: int) -> bool:
    return state.can_reach_region(RoomName.Sunchamber.value, player) and can_missile(state, player) and can_scan(state, player) and can_bomb(state, player)


def can_climb_sun_tower(state: CollectionState, player: int) -> bool:
    return can_spider(state, player) and can_super_missile(state, player)


def can_climb_tower_of_light(state: CollectionState, player: int) -> bool:
    return can_missile(state, player) and state.has(SuitUpgrade.Missile_Expansion.value, player, 8)
