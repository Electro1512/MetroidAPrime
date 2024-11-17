from BaseClasses import CollectionState
from .data.RoomNames import RoomName
from .Items import ProgressiveUpgrade, SuitUpgrade, get_progressive_upgrade_for_item
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from . import MetroidPrimeWorld


def has_required_artifact_count(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    required_count = world.options.required_artifacts.value
    return state.has_group("Artifacts", player, required_count)


def can_boost(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Boost_Ball.value], player)


def can_bomb(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Morph_Ball_Bomb.value], player)


def can_power_beam(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has_any([SuitUpgrade.Power_Beam.value, ProgressiveUpgrade.Progressive_Power_Beam.value], player)


def can_power_bomb(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    if world.options.main_power_bomb.value:
        return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Main_Power_Bomb.value], player)

    return state.has_all([SuitUpgrade.Power_Bomb_Expansion.value, SuitUpgrade.Morph_Ball.value], player)


def can_spider(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Spider_Ball.value, SuitUpgrade.Morph_Ball.value], player)


def can_missile(world: 'MetroidPrimeWorld', state: CollectionState, player: int, num_expansions: int = 1) -> bool:
    if world.options.missile_launcher.value:
        can_shoot = state.has(SuitUpgrade.Missile_Launcher.value, player)
        return can_shoot and (num_expansions <= 1 or state.has(SuitUpgrade.Missile_Expansion.value, player, num_expansions - 1))
    return state.has(SuitUpgrade.Missile_Expansion.value, player, num_expansions)


def can_super_missile(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return can_power_beam(world, state, player) \
        and can_missile(world, state, player) \
        and (state.has_all([SuitUpgrade.Charge_Beam.value, SuitUpgrade.Super_Missile.value], player)
             or state.has(ProgressiveUpgrade.Progressive_Power_Beam.value, player, 3))


def can_wave_beam(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has_any([SuitUpgrade.Wave_Beam.value, ProgressiveUpgrade.Progressive_Wave_Beam.value], player)


def can_ice_beam(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has_any([SuitUpgrade.Ice_Beam.value, ProgressiveUpgrade.Progressive_Ice_Beam.value], player)


def can_plasma_beam(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has_any([SuitUpgrade.Plasma_Beam.value, ProgressiveUpgrade.Progressive_Plasma_Beam.value], player)


def can_melt_ice(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return can_plasma_beam(world, state, player)


def can_grapple(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Grapple_Beam.value, player)


def can_space_jump(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Space_Jump_Boots.value, player)


def can_morph_ball(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Morph_Ball.value, player)


def can_xray(world: 'MetroidPrimeWorld', state: CollectionState, player: int, usually_required: bool = False, hard_required: bool = False) -> bool:
    if hard_required:
        return state.has(SuitUpgrade.X_Ray_Visor.value, player)
    if usually_required and world.options.remove_xray_requirements == "remove_all_but_omega_pirate":
        return True
    if usually_required:
        return state.has(SuitUpgrade.X_Ray_Visor.value, player)
    return bool(world.options.remove_xray_requirements.value) or state.has(SuitUpgrade.X_Ray_Visor.value, player)


def can_thermal(world: 'MetroidPrimeWorld', state: CollectionState, player: int, usually_required: bool = False, hard_required: bool = False) -> bool:
    if hard_required:
        return state.has(SuitUpgrade.Thermal_Visor.value, player)
    if usually_required and world.options.remove_thermal_requirements == "remove_all":
        return True
    if usually_required:
        return state.has(SuitUpgrade.Thermal_Visor.value, player)
    return bool(world.options.remove_thermal_requirements.value) or state.has(SuitUpgrade.Thermal_Visor.value, player)


def can_move_underwater(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Gravity_Suit.value, player)


def can_charge_beam(world: 'MetroidPrimeWorld', state: CollectionState, player: int, required_beam: Optional[SuitUpgrade] = None) -> bool:
    if required_beam is not None:
        progressive_item = get_progressive_upgrade_for_item(required_beam)
        assert progressive_item is not None
        return state.has_all([SuitUpgrade.Charge_Beam.value, required_beam.value], player) or state.has(progressive_item.value, player, 2)

    # If no beam is required, just check for Charge Beam or 2 of any progressive beam upgrade
    return state.has(SuitUpgrade.Charge_Beam.value, player) or state.has_any_count({upgrade.value: 2 for upgrade in ProgressiveUpgrade}, player)


def can_beam_combo(world: 'MetroidPrimeWorld', state: CollectionState, player: int, required_beam: SuitUpgrade) -> bool:
    if not can_missile(world, state, player, 2) or not can_charge_beam(world, state, player, required_beam):
        return False

    if required_beam == SuitUpgrade.Wave_Beam:
        return can_missile(world, state, player, 3) and (state.has(SuitUpgrade.Wavebuster.value, player) or state.has(ProgressiveUpgrade.Progressive_Wave_Beam.value, player, 3))
    elif required_beam == SuitUpgrade.Ice_Beam:
        return state.has(SuitUpgrade.Ice_Spreader.value, player) or state.has(ProgressiveUpgrade.Progressive_Ice_Beam.value, player, 3)
    elif required_beam == SuitUpgrade.Plasma_Beam:
        return can_missile(world, state, player, 3) and (state.has(SuitUpgrade.Flamethrower.value, player) or state.has(ProgressiveUpgrade.Progressive_Plasma_Beam.value, player, 3))
    else:
        raise ValueError(f"Invalid required beam: {required_beam}")


def can_scan(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Scan_Visor.value, player)


def can_heat(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    if world.options.non_varia_heat_damage.value:
        return state.has(SuitUpgrade.Varia_Suit.value, player)
    else:
        return state.has_any([SuitUpgrade.Varia_Suit.value, SuitUpgrade.Phazon_Suit.value, SuitUpgrade.Gravity_Suit.value], player)


def can_phazon(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Phazon_Suit.value, player)


def has_energy_tanks(world: 'MetroidPrimeWorld', state: CollectionState, player: int, count: int) -> bool:
    return state.has(SuitUpgrade.Energy_Tank.value, player, count)


def can_infinite_speed(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return can_boost(world, state, player) and can_bomb(world, state, player)


def can_defeat_sheegoth(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return can_bomb(world, state, player) or can_missile(world, state, player) or can_power_bomb(world, state, player) or can_plasma_beam(world, state, player)


def can_backwards_lower_mines(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    return bool(world.options.backwards_lower_mines.value)


def has_power_bomb_count(world: 'MetroidPrimeWorld', state: CollectionState, player: int, required_count: int) -> bool:
    count = state.count(SuitUpgrade.Power_Bomb_Expansion.value, player)
    if state.has(SuitUpgrade.Main_Power_Bomb.value, player):
        count += 4
    return count >= required_count


def can_warp_to_start(world: 'MetroidPrimeWorld', state: CollectionState, player: int) -> bool:
    SAVE_ROOMS = [
        RoomName.Landing_Site.value,
        RoomName.Save_Station_1.value,
        RoomName.Save_Station_2.value,
        RoomName.Save_Station_3.value,
        RoomName.Save_Station_Magmoor_A.value,
        RoomName.Save_Station_Magmoor_B.value,
        RoomName.Save_Station_A.value,
        RoomName.Save_Station_B.value,
        RoomName.Save_Station_C.value,
        RoomName.Save_Station_D.value,
        RoomName.Cargo_Freight_Lift_to_Deck_Gamma.value,
        RoomName.Save_Station_Mines_A.value,
        RoomName.Save_Station_Mines_B.value,
        RoomName.Save_Station_Mines_C.value,
    ]
    for room in SAVE_ROOMS:
        if state.can_reach_region(room, player):
            return True
    return False
