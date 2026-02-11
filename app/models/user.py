from pydantic import EmailStr
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional, TYPE_CHECKING
from app.core.enums.status_enum import Status

if TYPE_CHECKING:
    from app.models.skill import Skill
    from app.models.game_table import GameTable
    from app.models.user_groupf import UserGroupF

class User(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    username:str = Field(index=True, unique=True)
    email:Optional[EmailStr] = None
    full_name:str
    #admin:bool=Field(default=False)
    status:Status=Field(default=Status.active)
    hashed_password:str
    skill: Optional["Skill"] = Relationship(back_populates="user",
                                            sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    games: list["GameTable"] = Relationship(back_populates="user",
                                           sa_relationship_kwargs={"cascade": "all, delete-orphan",
                                                                   "foreign_keys": "[GameTable.user_id]"}
                                           )
    user_group: list["UserGroupF"] = Relationship(back_populates="user")
    



    
   