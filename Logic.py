from BaseClasses import CollectionState
from .data.RoomNames import RoomName
from .Items import ProgressiveUpgrade, SuitUpgrade, get_progressive_upgrade_for_item
import typing
if typing.TYPE_CHECKING:
    from .PrimeOptions import MetroidPrimeOptions


def _get_options(state: CollectionState, player: int) -> 'MetroidPrimeOptions':
    return state.multiworld.worlds[player].options


def has_required_artifact_count(state: CollectionState, player: int) -> bool:
    required_count = _get_options(state, player).required_artifacts.value
    return state.has_group("Artifacts", player, required_count)


def can_boost(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Boost_Ball.value], player)


def can_bomb(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Morph_Ball_Bomb.value], player)


def can_power_beam(state: CollectionState, player: int) -> bool:
    return state.has_any([SuitUpgrade.Power_Beam.value, ProgressiveUpgrade.Progressive_Power_Beam.value], player)


def can_power_bomb(state: CollectionState, player: int) -> bool:
    if _get_options(state, player).main_power_bomb.value:
        return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Main_Power_Bomb.value], player)

    return state.has_all([SuitUpgrade.Power_Bomb_Expansion.value, SuitUpgrade.Morph_Ball.value], player)


def can_spider(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Spider_Ball.value, SuitUpgrade.Morph_Ball.value], player)


def can_missile(state: CollectionState, player: int) -> bool:
    if _get_options(state, player).missile_launcher.value:
        return state.has(SuitUpgrade.Missile_Launcher.value, player)
    return state.has(SuitUpgrade.Missile_Expansion.value, player)


def can_super_missile(state: CollectionState, player: int) -> bool:
    return can_power_beam(state, player) \
        and can_missile(state, player) \
        and (state.has_all([SuitUpgrade.Charge_Beam.value, SuitUpgrade.Super_Missile.value], player)
             or state.has(ProgressiveUpgrade.Progressive_Power_Beam.value, player, 3))


def can_wave_beam(state: CollectionState, player: int) -> bool:
    return state.has_any([SuitUpgrade.Wave_Beam.value, ProgressiveUpgrade.Progressive_Wave_Beam.value], player)


def can_ice_beam(state: CollectionState, player: int) -> bool:
    return state.has_any([SuitUpgrade.Ice_Beam.value, ProgressiveUpgrade.Progressive_Ice_Beam.value], player)


def can_plasma_beam(state: CollectionState, player: int) -> bool:
    return state.has_any([SuitUpgrade.Plasma_Beam.value, ProgressiveUpgrade.Progressive_Plasma_Beam.value], player)


def can_melt_ice(state: CollectionState, player: int) -> bool:
    return can_plasma_beam(state, player)


def can_grapple(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Grapple_Beam.value, player)


def can_space_jump(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Space_Jump_Boots.value, player)


def can_morph_ball(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Morph_Ball.value, player)


def can_xray(state: CollectionState, player: int, hard_required: bool = False) -> bool:
    if hard_required:
        return state.has(SuitUpgrade.X_Ray_Visor.value, player)
    elif _get_options(state, player).remove_xray_requirements.value:
        return True
    return state.has(SuitUpgrade.X_Ray_Visor.value, player)


def can_thermal(state: CollectionState, player: int, hard_required: bool = False) -> bool:
    if hard_required:
        return state.has(SuitUpgrade.Thermal_Visor.value, player)
    elif _get_options(state, player).remove_thermal_requirements.value:
        return True
    return state.has(SuitUpgrade.Thermal_Visor.value, player)


def can_move_underwater(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Gravity_Suit.value, player)


def can_charge_beam(state: CollectionState, player: int, required_beam: typing.Optional[SuitUpgrade] = None) -> bool:
    if required_beam is not None:
        progressive_item = get_progressive_upgrade_for_item(required_beam)
        return state.has_all([SuitUpgrade.Charge_Beam.value, required_beam.value], player) or state.has(progressive_item.value, player, 2)

    # If no beam is required, just check for Charge Beam or 2 of any progressive beam upgrade
    return state.has(SuitUpgrade.Charge_Beam.value, player) or state.has_any_count({upgrade.value: 2 for upgrade in ProgressiveUpgrade}, player)


def can_scan(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Scan_Visor.value, player)


def can_crashed_frigate(state: CollectionState, player: int) -> bool:
    return can_bomb(state, player) and can_space_jump(state, player) and can_wave_beam(state, player) and can_move_underwater(state, player) and can_thermal(state, player)


def can_crashed_frigate_backwards(state: CollectionState, player: int) -> bool:
    return can_space_jump(state, player) and can_move_underwater(state, player) and can_bomb(state, player)


def can_heat(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Varia_Suit.value, player)


def can_phazon(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Phazon_Suit.value, player)


def has_energy_tanks(state: CollectionState, player: int, count: int) -> bool:
    return state.has(SuitUpgrade.Energy_Tank.value, player, count)


def can_infinite_speed(state: CollectionState, player: int) -> bool:
    return can_boost(state, player) and can_bomb(state, player)


def can_climb_tower_of_light(state: CollectionState, player: int) -> bool:
    return can_missile(state, player) and state.has(SuitUpgrade.Missile_Expansion.value, player, 8) and can_space_jump(state, player)


def can_defeat_sheegoth(state: CollectionState, player: int) -> bool:
    return can_bomb(state, player) or can_missile(state, player) or can_power_bomb(state, player) or can_plasma_beam(state, player)


def can_backwards_lower_mines(state, player) -> bool:
    return bool(_get_options(state, player).backwards_lower_mines.value)


def has_power_bomb_count(state: CollectionState, player: int, required_count: int) -> bool:
    count = state.count(SuitUpgrade.Power_Bomb_Expansion.value, player)
    if state.has(SuitUpgrade.Main_Power_Bomb.value, player):
        count += 4
    return count >= required_count