from pydantic import BaseModel,Field
from datetime import date
from app.core.enum.team_enum import TeamEnum

class MatchBase(BaseModel):
    match_date: date=None
    blue_score: int=None
    red_score: int=None
    

class MatchCreate (MatchBase):  
    season_id: int =None

class MatchUpdate (MatchBase):  
    id:int=None
    win:TeamEnum| None = Field(default=None)

class MatchRead(MatchBase):
    id:int=None
    win:TeamEnum| None = Field(default=None)
        