from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field
from typing import Optional

class User_base(SQLModel):
    username:str
    email:Optional[EmailStr] = None
    full_name:str
    admin:bool
    disable:bool

class User_create (User_base):  
    hashed_password:str

class User_update (User_base):  
    pass 

class User_read(User_base):
    id:int