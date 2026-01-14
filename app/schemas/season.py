from pydantic import BaseModel,Field


class SeasonBase(BaseModel):
    name: str = None # “Opening 2026”, “Closing 2026”
    year:int | None = Field(ge=1900, le=2100)
    is_active: bool  | None = Field(default=True)

 
class SeasonCreate (SeasonBase):  
    pass

class SeasonUpdate (SeasonBase):  
    id:int

class SeasonRead(SeasonBase):
    id:int
    



