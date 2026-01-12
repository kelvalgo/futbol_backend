from typing import Optional
from pydantic import BaseModel,Field
from app.core.enum.position_enum import PositionEnum


class SkillBase(BaseModel):
    position:PositionEnum  | None = Field(default=None)
    spatial_condition:bool = None
    gk : float | None=Field(default=None,ge=0, le=5)
    df : float | None=Field(default=None,ge=0, le=5)
    mf : float | None=Field(default=None,ge=0, le=5)
    wf : float | None=Field(default=None,ge=0, le=5)

class SkillCreate (SkillBase):  
    user_id: int 

class SkillUpdate (SkillBase):  
    id:int 

class SkillRead(SkillBase):
    id:int
    user_id: int = None
    