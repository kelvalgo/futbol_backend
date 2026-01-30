from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.group_friends import  GroupFriends
    from app.models.match_player import MatchPlayer


class Donation(SQLModel,table=True):

    id:int|None = Field(default=None, primary_key=True)
    grupo_id:int = Field(foreign_key="groupfriends.id")
    monto:float =Field(default=None)
    fecha:str=Field(default=None)
    referencia:str=Field(default=None)

    group_friends: "GroupFriends" =  Relationship(back_populates="donation")