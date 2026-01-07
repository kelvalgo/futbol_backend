from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.skill import Skill
    from app.models.game import Game

class User_base(SQLModel):
    username:str
    email:Optional[EmailStr] = None
    full_name:str
    admin:bool
    disable:bool

class User(User_base,table=True):
    id:int|None=Field(default=None,primary_key=True)
    hashed_password:str
    skill: Optional["Skill"] = Relationship(back_populates="user")
    games: Optional["Game"] = Relationship(back_populates="user")