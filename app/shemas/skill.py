from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,TYPE_CHECKING

class Skill_base(SQLModel):
    position:str
    spatial_condition:bool
    gk : float
    df : float 
    mf : float
    wf : float

class Skill_create (Skill_base):  
    pass 

class Skill_update (Skill_base):  
    pass 

class Skill(Skill_base,table=True):
    id:int
    user_id: int