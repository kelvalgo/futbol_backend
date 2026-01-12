from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime,timezone

if TYPE_CHECKING:
    from app.models.season import Season
    #from app.models.match_player import MatchPlayer

class Match(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    season_id: int = Field(foreign_key="season.id")

    match_date: datetime = Field(default_factory=timezone.utc)

    blue_score: int
    red_score: int

    season: Optional["Season"] = Relationship(back_populates="matches")

    #players: list["MatchPlayer"] = Relationship(back_populates="match")