from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class Table_base(SQLModel):
    games:int
    win:int
    lose : int
    tie : int 
    stars : float
    points : int
    fines: int

class Table_create (Table_base):  
    pass 

class Table_update (Table_base):  
    pass 

class Game(Table_base,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="user.id",
        unique=True  # 🔴 clave para 1 a 1
    )

    user: Optional["User"] = Relationship(back_populates="games")    