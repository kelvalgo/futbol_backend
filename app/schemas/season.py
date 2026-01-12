from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime,timezone


class SeasonBase(BaseModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str  # “Opening 2026”, “Closing 2026”
    year: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)


class SeasonCreate (SeasonBase):  
    user_id: int 

class SeasonUpdate (SeasonBase):  
    id:int 

class SeasonRead(SeasonBase):
    id:int
    user_id: int = None    



