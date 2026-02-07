from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date
from app.core.enums.status_enum import Status
from app.core.enums.team_enum import TeamEnum

if TYPE_CHECKING:
    from app.models.season import Season
    from app.models.match_player import MatchPlayer

class Match(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    season_id: int = Field(foreign_key="season.id")

    match_date: date

    blue_score: int
    red_score: int
    win:TeamEnum|None=Field(default=None)
    is_active: Status = Field(default=Status.active)

    season: Optional["Season"] = Relationship(back_populates="matches")

    players: list["MatchPlayer"] = Relationship(back_populates="match",
                                                sa_relationship_kwargs={"cascade": "all, delete-orphan"})