from BaseClasses import CollectionState
from worlds.metroidprime.PrimeOptions import CombatLogicDifficulty, MetroidPrimeOptions
from worlds.metroidprime.data.RoomNames import RoomName
from worlds.metroidprime.data.StartRoomData import StartRoomDifficulty
from .Items import SuitUpgrade, artifact_table


def _get_options(state: CollectionState, player: int) -> MetroidPrimeOptions:
    return state.multiworld.worlds[player].options


def has_required_artifact_count(state: CollectionState, player: int) -> bool:
    required_count = _get_options(state, player).required_artifacts.value
    return state.has_group("Artifacts", player, required_count)


def can_boost(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Boost_Ball.value], player)


def can_bomb(state: CollectionState, player: int) -> bool:
    return state.has_all([SuitUpgrade.Morph_Ball.value, SuitUpgrade.Morph_Ball_Bomb.value], player)


def can_power_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Power_Beam.value, player)


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
    return can_power_beam(state, player) and can_missile(state, player) and state.has_all([SuitUpgrade.Charge_Beam.value, SuitUpgrade.Super_Missile.value], player)


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


def can_charge_beam(state: CollectionState, player: int) -> bool:
    return state.has(SuitUpgrade.Charge_Beam.value, player)


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


def can_exit_ruined_shrine(state: CollectionState, player: int) -> bool:
    return can_morph_ball(state, player) or can_space_jump(state, player)


def can_flaahgra(state: CollectionState, player: int) -> bool:
    return state.can_reach_region(RoomName.Sunchamber.value, player) and can_missile(state, player) and can_scan(state, player) and (can_bomb(state, player) or (can_power_bomb(state, player) and has_power_bomb_count(state, player, 4)))


def can_climb_sun_tower(state: CollectionState, player: int) -> bool:
    return can_spider(state, player) and can_super_missile(state, player)


def can_climb_tower_of_light(state: CollectionState, player: int) -> bool:
    return can_missile(state, player) and state.has(SuitUpgrade.Missile_Expansion.value, player, 8) and can_missile(state, player)


def can_defeat_sheegoth(state: CollectionState, player: int) -> bool:
    return can_bomb(state, player) or can_missile(state, player) or can_power_bomb(state, player) or can_plasma_beam(state, player)


def can_backwards_lower_mines(state, player) -> bool:
    return bool(_get_options(state, player).backwards_lower_mines.value)


def has_power_bomb_count(state: CollectionState, player: int, required_count: int) -> bool:
    count = state.count(SuitUpgrade.Power_Bomb_Expansion.value, player)
    if state.has(SuitUpgrade.Main_Power_Bomb.value, player):
        count += 4
    return count >= required_count


def _can_combat_generic(state: CollectionState, player: int, normal_tanks: int, minimal_tanks: int, requires_charge_beam: bool = True) -> bool:
    difficulty = _get_options(state, player).combat_logic_difficulty.value
    if difficulty == CombatLogicDifficulty.NO_LOGIC:
        return True
    elif difficulty == CombatLogicDifficulty.NORMAL:
        return has_energy_tanks(state, player, normal_tanks) and (can_charge_beam(state, player) if requires_charge_beam else True)
    elif difficulty == CombatLogicDifficulty.MINIMAL:
        return has_energy_tanks(state, player, minimal_tanks) and (can_charge_beam(state, player) if requires_charge_beam else True)


def can_combat_mines(state: CollectionState, player: int) -> bool:
    return _can_combat_generic(state, player, 5, 3)


def can_combat_labs(state: CollectionState, player: int) -> bool:
    if _get_options(state, player).starting_room.value == StartRoomDifficulty.Buckle_Up.value:
        return True
    return _can_combat_generic(state, player, 3, 1)


def can_combat_thardus(state: CollectionState, player: int) -> bool:
    if _get_options(state, player).starting_room.value == StartRoomDifficulty.Buckle_Up.value:
        return True
    return _can_combat_generic(state, player, 5, 2)


def can_combat_flaaghra(state: CollectionState, player: int) -> bool:
    if _get_options(state, player).starting_room.value == StartRoomDifficulty.Buckle_Up.value:
        return True
    return _can_combat_generic(state, player, 3, 2, requires_charge_beam=False)


def can_combat_ridley(state: CollectionState, player: int) -> bool:
    return _can_combat_generic(state, player, 10, 8)


def can_combat_prime(state: CollectionState, player: int) -> bool:
    return _can_combat_generic(state, player, 10, 5)


def can_combat_ghosts(state: CollectionState, player: int) -> bool:
    difficulty = _get_options(state, player).combat_logic_difficulty.value
    if difficulty == CombatLogicDifficulty.NO_LOGIC:
        return True
    elif difficulty == CombatLogicDifficulty.NORMAL:
        return can_charge_beam(state, player) and can_power_beam(state, player) and can_xray(state, player, True)
    elif difficulty == CombatLogicDifficulty.MINIMAL:
        return (can_charge_beam(state, player) and can_power_beam(state, player) or can_xray(state, player, True))
