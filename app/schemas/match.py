from pydantic import BaseModel,Field
from datetime import date
from app.core.enums.match_status import MatchStatus, MatchStatusFinished
from app.core.enums.team_enum import TeamEnum
from typing import Optional

from app.core.enums.team_win_tie_lie_enum import TeamWinTieLieEnum

class MatchBase(BaseModel):

    match_date: int | None =None
    blue_score: int | None =None
    red_score: int | None =None
    

class MatchCreate (BaseModel):  
    season_id: int
    match_date: date

class MatchCreateBD (BaseModel):  
    season_id: int
    match_date: str    


class MatchUpdatePatch (BaseModel):  
    match_date: Optional[str]
    blue_score: Optional[int]
    red_score: Optional[int]
    win:Optional["TeamWinTieLieEnum"]
    status_match: Optional["MatchStatus"]

class MatchUpdateFinishPatch (BaseModel):
    blue_score: Optional[int]
    red_score: Optional[int]
    win:Optional["TeamWinTieLieEnum"]
    status_match: Optional["MatchStatusFinished"]    

class MatchUpdatePatchRating (BaseModel):      
    team_rating_red:Optional[float]
    team_rating_blue:Optional[float]
    status_match: Optional["MatchStatus"]


class MatchRead(MatchBase):
    id:int | None =None
    win:TeamEnum| None = Field(default=None)
        