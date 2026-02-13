from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,TYPE_CHECKING
from sqlalchemy import CheckConstraint,UniqueConstraint
from sqlalchemy import Column, ForeignKey

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.season import Season

class GameTable(SQLModel,table=True):
    id: int|None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    season_id: int = Field(
        sa_column=Column(
            ForeignKey("season.id", ondelete="CASCADE"),
            nullable=False
        )
    )

    games:int
    win:int
    lose : int
    tie : int 

    player_goals_scored: int = Field(default=0)
    goalkeeper_goals_conceded: int = Field(default=0)

    stars : float  
    points : int
    fines: int

    user: Optional["User"] = Relationship(
        back_populates="games",
        sa_relationship_kwargs={"foreign_keys": "[GameTable.user_id]"}
        )
    season: Optional["Season"] = Relationship(back_populates="game_table")   

    __table_args__ = (
        CheckConstraint("stars BETWEEN 0 AND 5", name="stars_range"),
        UniqueConstraint("user_id", "season_id", name="uix_user_season"),)