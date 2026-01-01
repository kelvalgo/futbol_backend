from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field
from typing import Optional

class User_base(SQLModel):
    username:str
    email:Optional[EmailStr] = None
    full_name:str
    admin:bool
    disable:bool

class User(User_base,table=True):
    id:int|None=Field(default=None,primary_key=True)
    hashed_password:str