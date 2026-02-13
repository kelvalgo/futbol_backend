from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,TYPE_CHECKING
from sqlalchemy import CheckConstraint
from app.core.enums.position_enum import PositionEnum
from sqlalchemy import Column, ForeignKey

if TYPE_CHECKING:
    from app.models.user_groupf import UserGroupF

class Skill(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    user_group_id: int = Field(
        sa_column=Column(
            ForeignKey("usergroupf.id", ondelete="CASCADE"),
            unique=True,
            nullable=False
        )
    )
    position:PositionEnum = Field(default=None)
    spatial_condition:bool=Field(default=False)
    gk : float
    df : float
    mf : float
    wf : float

    user_group: Optional["UserGroupF"] = Relationship(
        back_populates="skill"
    )

    __table_args__ = (
        CheckConstraint("gk BETWEEN 0 AND 5", name="gk_range"),
        CheckConstraint("df BETWEEN 0 AND 5", name="df_range"),
        CheckConstraint("mf BETWEEN 0 AND 5", name="mf_range"),
        CheckConstraint("wf BETWEEN 0 AND 5", name="wf_range"),
    )