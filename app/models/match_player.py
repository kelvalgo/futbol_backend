from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from app.core.enum.team_enum import TeamEnum

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.match import Match

class MatchPlayer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    match_id: int = Field(foreign_key="match.id")
    user_id: int = Field(foreign_key="user.id")

    # ⚽ action of player
    team:TeamEnum = Field(default=None)
    goals_scored: int = Field(default=0)
    goals_conceded_as_goalkeeper: int = Field(default=0)
    is_goalkeeper: bool = Field(default=False)

    match: Optional["Match"] = Relationship(back_populates="players")
    user: Optional["User"] = Relationship()