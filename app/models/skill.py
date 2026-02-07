from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,TYPE_CHECKING
from sqlalchemy import CheckConstraint
from app.core.enums.position_enum import PositionEnum

if TYPE_CHECKING:
    from app.models.user import User

class Skill(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    user_id: int = Field(
        foreign_key="user.id",
        unique=True  # 🔴 clave para 1 a 1
    )
    position:PositionEnum = Field(default=None)
    spatial_condition:bool=Field(default=False)
    gk : float
    df : float
    mf : float
    wf : float

    user: Optional["User"] = Relationship(back_populates="skill")

    __table_args__ = (
        CheckConstraint("gk BETWEEN 0 AND 5", name="gk_range"),
        CheckConstraint("df BETWEEN 0 AND 5", name="df_range"),
        CheckConstraint("mf BETWEEN 0 AND 5", name="mf_range"),
        CheckConstraint("wf BETWEEN 0 AND 5", name="wf_range"),
    )