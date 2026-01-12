from pydantic import BaseModel,Field
from typing import Optional


class GameTableBase(BaseModel):
    games:int =None
    win:int=None
    lose : int=None
    tie : int    =None 
    player_goals_scored: int = Field(default=0)
    goalkeeper_goals_conceded: int = Field(default=0)
    stars : float=Field(default=None,ge=0, le=5)  
    points : int =None
    fines: int =None

class GameTableCreate (GameTableBase):  
    user_id: int 
    season_id:int

class GameTableUpdate (GameTableBase):  
    id:int 

class GameTableUpdatePatch ():  
    id:int    

class GameTableRead(GameTableBase):
    id:int
    user_id: int
    season_id:int 


    