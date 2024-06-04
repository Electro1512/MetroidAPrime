from enum import Enum

class TrickDifficulty(Enum):
  Easy = 0
  Medium = 1
  Hard = 2

class Trick(Enum):
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