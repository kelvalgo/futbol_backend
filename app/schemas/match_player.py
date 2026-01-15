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

class MatchPlayerUpdatePut (BaseModel):  
    id: int
    match_id: int 
    user_id: int
    team:TeamEnum 
    position:PositionEnum
    matchResult:MatchResult
    goals_scored: int
    goals_conceded_as_goalkeeper: int

class MatchPlayerUpdatePatch (MatchPlayer):  
    id: int 
    match_id: int 
    user_id: int 
  
   


class MatchPlayerRead(MatchPlayer):
    id: int = None 
    match_id: int = None
    user_id: int = None   







