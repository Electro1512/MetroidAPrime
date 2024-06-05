from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

from BaseClasses import CollectionState
from worlds.metroidprime.Items import SuitUpgrade
from worlds.metroidprime.Logic2 import can_bomb, can_boost, can_morph_ball, can_scan, can_space_jump, can_thermal, can_wave_beam


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
                                              lambda state, player: can_morph_ball(state, player) and can_space_jump(state, player) and can_wave_beam(state, player) and can_thermal(state, player) and can_boost(state, player))

    frigate_crash_site_scan_dash: TrickInfo = TrickInfo("Crashed Frigate Scan Dash", "Perform a scan dash to reach the item at Crashed Frigate", TrickDifficulty.Hard, can_scan)

    frigate_crash_site_slope_jump: TrickInfo = TrickInfo("Crashed Frigate Slope Jump", "Perform a slope jump to reach the item at Crashed Frigate", TrickDifficulty.Easy, can_space_jump)

    frigate_crash_site_climb_to_overgrown_cavern: TrickInfo = TrickInfo("Crashed Frigate Climb to Overgrown Cavern", "Climb to Overgrown Cavern", TrickDifficulty.Medium,
                                                                        lambda state, player: can_bomb(state, player) and can_space_jump(state, player))
    great_tree_hall_skip_bars: TrickInfo = TrickInfo("Great Tree Hall Skip Bars", "Skip the bars in Great Tree Hall using Morph Ball Bombs", TrickDifficulty.Hard, can_bomb)

    great_tree_chamber_no_xray: TrickInfo = TrickInfo("Great Tree Chamber No XRay", "Reach the Great Tree Chamber without XRay Visor", TrickDifficulty.Easy, can_space_jump)

    great_tree_hall_no_spider_ball: TrickInfo = TrickInfo("Great Tree Hall No Spider Ball", "Reach the door to the Life Grove Tunnel without Spider Ball", TrickDifficulty.Easy, can_space_jump)

    root_cave_arbor_chamber_no_grapple_xray: TrickInfo = TrickInfo("Root Cave Arbor Chamber No Grapple XRay", "Reach the Arbor Chamber without Grapple Beam or XRay Visor using a Combat Dash", TrickDifficulty.Hard, lambda state, player: can_space_jump(state, player) and can_scan(state, player))
  # Chozo
  # Magmoor
  # Phendrana
  # Phazon Mines
