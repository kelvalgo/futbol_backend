from typing import Optional

from pydantic import BaseModel,Field

from app.core.enums.status_enum import Status


class SeasonBase(BaseModel):
    name: str = None # “Opening 2026”, “Closing 2026”
    year:int | None = Field(ge=1900, le=2100)
    is_active:Status

 
class SeasonCreate (BaseModel):  
    name: str = None # “Opening 2026”, “Closing 2026”  



class SeasonUpdatePatch (BaseModel): 
    name:  Optional[str]=None  # “Opening 2026”, “Closing 2026”
    is_active:Optional[Status]=None

class SeasonRead(SeasonBase):
    id:int
    



