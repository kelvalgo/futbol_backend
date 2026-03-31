from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date
from app.core.enums.match_status import MatchStatus
from app.core.enums.status_enum import Status
from app.core.enums.team_enum import TeamEnum
from sqlalchemy import Column, ForeignKey

if TYPE_CHECKING:
    from app.models.season import Season
    from app.models.match_player import MatchPlayer

class Match(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    season_id: int = Field(
    sa_column=Column(
        ForeignKey("season.id", ondelete="CASCADE"),
        nullable=False
        )
    )   

    match_date: str=Field(nullable=True)

    blue_score: int= Field(default=0)
    red_score: int= Field(default=0)
    win:TeamEnum|None=Field(default=None)
    status_match: MatchStatus = Field(default=MatchStatus.scheduled)
    team_rating_red:Optional[float]=Field(default=0.0)
    team_rating_blue:Optional[float]=Field(default=0.0)

    season: Optional["Season"] = Relationship(back_populates="matches")

    players: list["MatchPlayer"] = Relationship(back_populates="match",
                                                sa_relationship_kwargs={"cascade": "all, delete-orphan"})