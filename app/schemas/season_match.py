from pydantic import BaseModel,Field
from datetime import date
from app.core.enums.match_status import MatchStatus
from app.core.enums.team_enum import TeamEnum
from typing import Optional


class SeasonMatchRead(BaseModel):

    id_match:int
    id_season:int
    name_season:str
    match_date:str
    blue_score:Optional[int]
    team_rating_blue:Optional[float]
    red_score: Optional[int]    
    team_rating_red:Optional[float]    
    win:Optional["TeamEnum"]
    status_match:Optional["MatchStatus"]