from pydantic import BaseModel
from app.core.enum.match_result import MatchResult
from app.core.enum.position_enum import PositionEnum
from app.core.enum.team_enum import TeamEnum

class MatchPlayer(BaseModel):   

    # ⚽ action of player
    team:TeamEnum = None
    position:PositionEnum= None
    matchResult:MatchResult= None
    goals_scored: int =None
    goals_conceded_as_goalkeeper: int= None

   
class MatchPlayerCreate (MatchPlayer):  
    match_id: int = None
    user_id: int = None

class MatchPlayerUpdate (MatchPlayer):  
    id: int = None 
    match_id: int = None
    user_id: int = None    
   


class MatchPlayerRead(MatchPlayer):
    id: int = None 
    match_id: int = None
    user_id: int = None   







