from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

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
    id:int|None=Field(default=None,primary_key=True)
    user_id: int = Field(
        foreign_key="user.id",
        unique=True  # 🔴 clave para 1 a 1
    )

    user: Optional["User"] = Relationship(back_populates="skill")