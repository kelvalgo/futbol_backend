from pydantic import BaseModel,Field
from datetime import date
from app.core.enums.team_enum import TeamEnum

class MatchBase(BaseModel):

    match_date: date=None
    blue_score: int=None
    red_score: int=None
    

class MatchCreate (MatchBase):  
    season_id: int =None

class MatchUpdatePut (BaseModel):  
    id:int=None
    win:TeamEnum
    is_active: bool
    match_date: date
    blue_score: int
    red_score: int

class MatchUpdatePatch (MatchBase):  
    id:int=None
    win:TeamEnum| None = Field(default=None) 
    is_active: bool | None = Field(default=True) 

class MatchRead(MatchBase):
    id:int=None
    win:TeamEnum| None = Field(default=None)
        