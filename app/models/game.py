from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class Game(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="user.id",
        unique=True  # 🔴 clave para 1 a 1
    )
    games:int
    win:int
    lose : int
    tie : int 
    stars : float
    points : int
    fines: int

    user: Optional["User"] = Relationship(back_populates="games")    