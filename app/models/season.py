from sqlmodel import SQLModel,Field,Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game_table import GameTable
    from app.models.match import Match
    from app.models.group_friends import GroupFriends

class Season(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str  # “Opening 2026”, “Closing 2026”
    year: int = Field(ge=1900, le=2100)
    is_active: bool = Field(default=True)

    group_id: int = Field(default=None, foreign_key="groupfriends.id")

    game_table: list["GameTable"] = Relationship(back_populates="season",
                                            sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    matches: list["Match"] = Relationship(back_populates="season",
                                            sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    group_friends: "GroupFriends" = Relationship(back_populates="seasons")