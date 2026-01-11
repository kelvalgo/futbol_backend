from pydantic import EmailStr
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.skill import Skill
    from app.models.game import Game

class User(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    username:str = Field(index=True, unique=True)
    email:Optional[EmailStr] = None
    full_name:str
    admin:bool=Field(default=False)
    disable:bool
    hashed_password:str
    skill: Optional["Skill"] = Relationship(back_populates="user",
                                            sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    games: Optional["Game"] = Relationship(back_populates="user",
                                           sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    



    
   