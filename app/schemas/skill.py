from typing import Optional

from pydantic import BaseModel,Field
from app.core.enums.position_enum import PositionEnum


class SkillBase(BaseModel):
    position:PositionEnum  
    spatial_condition:bool
    gk : float =Field(ge=0, le=5)
    df : float =Field(ge=0, le=5)
    mf : float =Field(ge=0, le=5)
    wf : float =Field(ge=0, le=5)

class SkillCreate (BaseModel):  
    user_id: int
    position:PositionEnum  
    spatial_condition:bool
    gk : float =Field(ge=0, le=5)
    df : float =Field(ge=0, le=5)
    mf : float =Field(ge=0, le=5)
    wf : float =Field(ge=0, le=5) 
    

class SkillUpdatePatch (BaseModel):  
    user_id:int
    position: Optional[PositionEnum] = None
    spatial_condition: Optional[bool] = None
    gk: Optional[float] = Field(default=None, ge=0, le=5)
    df: Optional[float] = Field(default=None, ge=0, le=5)
    mf: Optional[float] = Field(default=None, ge=0, le=5)
    wf: Optional[float] = Field(default=None, ge=0, le=5) 

class SkillRead(BaseModel):
    id:int 
    user_id:int
    user_name:str
    position:PositionEnum  
    spatial_condition:bool
    gk : float =Field(ge=0, le=5)
    df : float =Field(ge=0, le=5)
    mf : float =Field(ge=0, le=5)
    wf : float =Field(ge=0, le=5)
    