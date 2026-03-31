from pydantic import BaseModel
from app.core.enums.match_result import MatchResult
from app.core.enums.position_enum import PositionEnum
from app.core.enums.team_enum import TeamEnum

class MatchPlayer(BaseModel):   

    # ⚽ action of player
    team:TeamEnum = None
    position:PositionEnum= None
    goals_scored: int =None
    goals_conceded_as_goalkeeper: int= None

   
class MatchPlayerCreate (BaseModel):  
    match_id: int = None
    user_id: int = None
    team:TeamEnum = None
    position:PositionEnum= None
    goals_scored: int =None
    goals_conceded_as_goalkeeper: int= None

class MatchPlayerUpdatePut (BaseModel):  
    id: int
    match_id: int 
    user_id: int
    team:TeamEnum 
    position:PositionEnum
    goals_scored: int
    goals_conceded_as_goalkeeper: int

class MatchPlayerUpdatePatch (MatchPlayer):  
    id: int 
    match_id: int 
    user_id: int     
   


class MatchPlayerRead(BaseModel):
    id: int
    match_id: int 
    user_id: int
    username:str
    team:TeamEnum 
    position:PositionEnum
    goals_scored: int
    goals_conceded_as_goalkeeper: int 









