from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field
from typing import Optional

class User_base(SQLModel):
    username:str = None
    email:Optional[EmailStr] = None
    full_name:str = None
    admin:bool = None
    disable:bool = None

class User_create (User_base):  
    pass


class User_update (User_base):  
    pass

class User_read(User_base):
    id:int