from typing import Optional
from pydantic import BaseModel,Field
from app.core.enum.position_enum import PositionEnum


class Skill_base(BaseModel):
    position:PositionEnum = Field(default=None)
    spatial_condition:bool = None
    gk : Optional[float]=Field(default=None,ge=0, le=5)
    df : Optional[float]=Field(default=None,ge=0, le=5)
    mf : Optional[float]=Field(default=None,ge=0, le=5)
    wf : Optional[float]=Field(default=None,ge=0, le=5)

class Skill_create (Skill_base):  
    user_id: int 

class Skill_update (Skill_base):  
    id:int 

class Skill_read(Skill_base):
    id:int
    user_id: int = None
    