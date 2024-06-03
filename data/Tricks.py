from enum import Enum

class TrickDifficulty(Enum):
  Easy = 0
  Medium = 1
  Hard = 2

class Trick(Enum):
  L_Jump = "L-Jump"
  R_Jump = "R-Jump"
  Infinite_Speed = "Infinite Speed"