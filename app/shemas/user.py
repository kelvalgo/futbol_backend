from pydantic import BaseModel,EmailStr
from typing import Optional

class User_base(BaseModel):
    username:str = None
    email:Optional[EmailStr] = None
    full_name:str = None
    admin:bool = None
    disable:bool = None

class User_create (User_base):  
    pass


class User_update (User_base):  
    id:int

class User_read(User_base):
    id:int