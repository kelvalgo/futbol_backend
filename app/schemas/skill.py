from typing import Optional
from pydantic import BaseModel,Field
from app.core.enum.position_enum import PositionEnum


class SkillBase(BaseModel):
    position:PositionEnum = Field(default=None)
    spatial_condition:bool = None
    gk : float=Field(default=None,ge=0, le=5)
    df : float=Field(default=None,ge=0, le=5)
    mf : float=Field(default=None,ge=0, le=5)
    wf : float=Field(default=None,ge=0, le=5)

class SkillCreate (SkillBase):  
    user_id: int 

class SkillUpdate (SkillBase):  
    id:int 

class SkillRead(SkillBase):
    id:int
    user_id: int = None
    