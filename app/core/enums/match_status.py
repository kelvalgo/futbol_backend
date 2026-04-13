from enum import Enum

class MatchStatus(str, Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    in_progress = "in_progress"

class MatchStatusFinished(str, Enum):    
    finished = "finished"

class MatchStatusRead(str, Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    in_progress = "in_progress"   
    finished = "finished" 
