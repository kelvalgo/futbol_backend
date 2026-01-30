from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from app.core.enum.rol import Rol
from sqlalchemy import CheckConstraint, UniqueConstraint

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.group_friends import GroupFriends



class UserGroupF(SQLModel,table=True):

    id:int|None = Field(default=None, primary_key=True)


    user_id:int = Field(
        foreign_key="user.id",
        unique=True  # 🔴 clave para 1 a 1
    )
    group_id:int = Field(
        foreign_key="groupfriends.id",
        unique=True  # 🔴 clave para 1 a 1
    )

    rol: Rol=Field(default=None)  # admin | user
    disable:bool =Field(default=False)
    fecha_ingreso:str=Field(default=None)

    user:"User" = Relationship(back_populates="user_group")
    group_friends:"GroupFriends" = Relationship(back_populates="user_group")

    __table_args__ = (
        UniqueConstraint("user_id", "group_id"),
    )