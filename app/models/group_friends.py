from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.donation import Donation
    from app.models.user_groupf import UserGroupF
    from app.models.season import Season



class GroupFriends(SQLModel, table=True):

    id:int|None = Field(default=None, primary_key=True)
    name:str=Field(default=None)
    description:str =Field(default=None)
    date_creation:str=Field(default=None)
    last_date_donation: Optional[str] = Field(default=None)
    perioding_donation:int = Field(default=30)  # días
    activo: bool = Field(default=True)

    donation: list["Donation"] = Relationship(back_populates="group_friends")

    user_group:list["UserGroupF"]=Relationship(back_populates="group_friends",
                                            sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    
    seasons: list["Season"] = Relationship(back_populates="group_friends",
                                            sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    
    
    