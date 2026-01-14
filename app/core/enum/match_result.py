from enum import Enum

class MatchResult(str, Enum):
    WIN = "win"
    LOSE = "lose"
    Tie = "tie"