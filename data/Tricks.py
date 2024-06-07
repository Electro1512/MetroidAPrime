from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

from BaseClasses import CollectionState
from worlds.metroidprime.Items import SuitUpgrade
from worlds.metroidprime.Logic2 import can_bomb, can_boost, can_grapple, can_ice_beam, can_infinite_speed, can_morph_ball, can_plasma_beam, can_power_bomb, can_scan, can_space_jump, can_spider, can_thermal, can_wave_beam


class TrickDifficulty(Enum):
    No_Tricks = -1
    Easy = 0
    Medium = 1
    Hard = 2


class Trick_Type(Enum):
    L_Jump = "L Jump"
    L_Jump_Space_Jump = "L-Jump Space Jump"
    R_Jump = "R-Jump"
    R_Jump_Space_Jump = "R-Jump Space Jump"
    Scan_Dash = "Scan Dash"
    Scan_Dash_Space_Jump = "Scan Dash"
    Slope_Jump_With_Space_Jump = "Slope Jump With Space Jump"
    Slope_Jump = "Slope Jump No Space Jump"
    Combat_Dash = "Combat Dash"
    Combat_Dash_Space_Jump = "Combat Dash"
    Infinite_Speed = "Infinite Speed"
    Double_Bomb_Jump = "Double Bomb Jump"
    No_XRay = "No XRay"


@dataclass
class TrickInfo:
    name: str
    description: str
    difficulty: TrickDifficulty
    rule_func: Callable[[CollectionState, int], bool]


@dataclass
class Tricks:
  # Tallon
    alcove_escape: TrickInfo = TrickInfo("Alcove Escape", "Escape the Alcove without space jump", TrickDifficulty.Medium, lambda state, player: True)
    landing_site_scan_dash: TrickInfo = TrickInfo("Landing Site Scan Dash", "Perform a scan dash to reach the landing site without bombs", TrickDifficulty.Medium, can_scan)

    frigate_no_gravity: TrickInfo = TrickInfo("Frigate No Gravity", "Complete the Frigate without Gravity Suit", TrickDifficulty.Medium,
                                              lambda state, player: can_bomb(state, player) and can_space_jump(state, player) and can_wave_beam(state, player) and can_thermal(state, player))

    hydro_access_tunnel_no_gravity: TrickInfo = TrickInfo("Hydro Access Tunnel No Gravity", "Complete the Hydro Access Tunnel without Gravity Suit using Wall Boosting", TrickDifficulty.Hard,
                                                          lambda state, player: can_boost(state, player))

    frigate_backwards_no_gravity: TrickInfo = TrickInfo("Frigate No Gravity", "Complete the Frigate without Gravity Suit", TrickDifficulty.Medium,
                                                        lambda state, player: can_morph_ball(state, player) and can_space_jump(state, player) and can_boost(state, player))

    frigate_crash_site_scan_dash: TrickInfo = TrickInfo("Crashed Frigate Scan Dash", "Perform a scan dash to reach the item at Crashed Frigate", TrickDifficulty.Hard, can_scan)

    frigate_crash_site_slope_jump: TrickInfo = TrickInfo("Crashed Frigate Slope Jump", "Perform a slope jump to reach the item at Crashed Frigate", TrickDifficulty.Easy, can_space_jump)

    frigate_crash_site_climb_to_overgrown_cavern: TrickInfo = TrickInfo("Crashed Frigate Climb to Overgrown Cavern", "Climb to Overgrown Cavern", TrickDifficulty.Medium,
                                                                        lambda state, player: can_bomb(state, player) and can_space_jump(state, player))
    great_tree_hall_skip_bars: TrickInfo = TrickInfo("Great Tree Hall Skip Bars", "Skip the bars in Great Tree Hall using Morph Ball Bombs", TrickDifficulty.Hard, can_bomb)

    great_tree_chamber_no_xray: TrickInfo = TrickInfo("Great Tree Chamber No XRay", "Reach the Great Tree Chamber without XRay Visor", TrickDifficulty.Easy, can_space_jump)

    great_tree_hall_no_spider_ball: TrickInfo = TrickInfo("Great Tree Hall No Spider Ball", "Reach the door to the Life Grove Tunnel without Spider Ball", TrickDifficulty.Easy, can_space_jump)

    root_cave_arbor_chamber_no_grapple_xray: TrickInfo = TrickInfo("Root Cave Arbor Chamber No Grapple XRay", "Reach the Arbor Chamber without Grapple Beam or XRay Visor using a Combat Dash", TrickDifficulty.Hard, lambda state, player: can_space_jump(state, player) and can_scan(state, player))
  # Chozo
    vault_via_plaza: TrickInfo = TrickInfo("Vault Via Plaza", "Reach the Vault via the Main Plaza using an L Jump", TrickDifficulty.Easy, can_space_jump)
    plaza_half_pipe_no_boost: TrickInfo = TrickInfo("Plaza Half Pipe No Boost", "Reach the Half Pipe in the Main Plaza using a slope jump", TrickDifficulty.Easy, can_space_jump)
    plaza_grapple_ledge_r_jump: TrickInfo = TrickInfo("Plaza Grapple Ledge R Jump", "Reach the Grapple Ledge in the Main Plaza using an R Jump", TrickDifficulty.Easy, can_space_jump)

    ruined_shrine_upper_door_no_spider_ball: TrickInfo = TrickInfo("Ruined Shrine Upper Door L Jump", "Reach the upper door in the Ruined Shrine by L Jumping off the root", TrickDifficulty.Easy, can_space_jump)
    ruined_shrine_upper_door_scan_dash: TrickInfo = TrickInfo("Ruined Shrine Upper Door Scan Dash", "Reach the upper door in the Ruined Shrine by scan dashing without space jump", TrickDifficulty.Hard, can_scan)
    ruined_shrine_scan_dash_escape: TrickInfo = TrickInfo("Ruined Shrine Scan Dash Escape", "Escape the Ruined Shrine by scan dashing  off the branches", TrickDifficulty.Easy, can_scan)

    tower_of_light_climb_without_missiles: TrickInfo = TrickInfo("Tower of Light Climb Without Missiles", "Tower of Light can be climbed by dashing to the outside edges, skipping the 40 missile requirement.", TrickDifficulty.Easy, can_space_jump)
    tower_chamber_no_gravity: TrickInfo = TrickInfo("Tower Chamber No Gravity", "Reach the Tower Chamber without Gravity Suit by using a slope jump", TrickDifficulty.Easy, can_space_jump)

    ruined_nursery_no_bombs: TrickInfo = TrickInfo("Ruined Nursery No Bombs", "Reach the Ruined Nursery Item by space jumping and morphing near the item", TrickDifficulty.Hard, lambda state, player: can_space_jump(state, player) and can_morph_ball(state, player))

    magma_pool_scan_dash: TrickInfo = TrickInfo("Cross Magma Pool Suitless", "Cross magma pool using a scan dash on the crate items", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and can_scan(state, player))
    magma_pool_item_scan_dash: TrickInfo = TrickInfo("Magma Pool Item No Grapple", "Use the scan dash and a power bomb to get the item in the magma pool", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and can_scan(state, player) and can_power_bomb(state, player))
    magma_pool_item_infinite_speed: TrickInfo = TrickInfo("Magma Pool Item Infinite Speed", "Use infinite speed to get the item in the magma pool", TrickDifficulty.Medium, can_infinite_speed)

    arboretum_scan_gate_skip: TrickInfo = TrickInfo("Arboretum Scan Gate Skip", "Skip the gate in the Arboretum by double bomb jumping", TrickDifficulty.Easy, can_bomb)

    gathering_hall_without_space_jump: TrickInfo = TrickInfo("Gathering Hall Without Space Jump", "Double bomb jump from the side platform to the grate where the item is", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_power_bomb(state, player))

    watery_hall_no_gravity: TrickInfo = TrickInfo("Watery Hall No Gravity", "Reach the Watery Hall Underwater Item without Gravity Suit by using a slope jump", TrickDifficulty.Easy, can_space_jump)

    furnace_no_spider_ball = TrickInfo("Furnace No Spider Ball", "Reach the Item inside the Furnace without Spider Ball by jumping on the side of the spider track", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player))
    furnace_spider_track_hbj = TrickInfo("Furnace Spider Track HBJ", "Reach the first track in furnace with a hyper bomb jump", TrickDifficulty.Medium, lambda state, player: can_bomb(state, player) and can_spider(state, player))
    furnace_spider_track_sj_bombs = TrickInfo("Furnace Spider Track SJ Bombs", "You can climb the Furnace and its spider tracks using Space Jump, reach the top of the room, then bomb jump across to the item.", TrickDifficulty.Medium, lambda state, player: can_bomb(state, player) and can_space_jump(state, player))

    crossway_item_fewer_reqs = TrickInfo("Crossway Item Fewer Reqs", "Reach the crossway item using only SJB and Morph Ball", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_space_jump(state, player))
    crossway_hpbj = TrickInfo("Crossway Half pip bomb jump", "Reach the hall of the elders using a half pipe bomb jump", TrickDifficulty.Hard, lambda state, player: can_bomb(state, player))

    hall_of_elders_bomb_slots_no_spider = TrickInfo("Hall of Elders No Spider Ball", "Reach the bomb slots without the spider ball by jumping on a peg to activate the top bomb slot", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player) and can_bomb(state, player))
    hall_of_elders_reflecting_pool_no_spider = TrickInfo("Hall of Elders Reflecting Pool No Spider Ball", "Reach the reflecting pool without the spider ball", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player) and can_wave_beam(state, player) and can_bomb(state, player))
    hall_of_elders_reflecting_pool_no_wave_beam = TrickInfo("Hall of Elders Reflecting Pool No Wave Beam", "In Hall of the Elders, you can Hyper Bomb Jump (HBJ) to the morph ball track and reach the door to Reflecting Pool Access.", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and can_bomb(state, player))

    hall_of_elders_elder_chamber_no_spider = TrickInfo("Hall of Elders Elder Chamber No Spider Ball", "Reach the bomb slots without the spider ball by jumping on a peg to activate the top bomb slot", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_plasma_beam(state, player) and can_space_jump(state, player))
    hall_of_elders_item_no_spider = TrickInfo("Hall of Elders Item No Spider Ball", "Reach the bomb slots without the spider ball by jumping on a peg to activate the top bomb slot", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_ice_beam(state, player) and can_space_jump(state, player))

    reflecting_pool_space_jump_climb = TrickInfo("Reflecting Pool Space Jump Climb", "Climb the reflecting pool by space jumping off a stone toad", TrickDifficulty.Easy, can_space_jump)

  # Magmoor
  # Phendrana
  # Phazon Mines
