from enum import Enum

class MatchStatus(str, Enum):
    scheduled = "scheduled"
    finished = "finished"
    cancelled = "cancelled"
    in_progress = "in_progress"