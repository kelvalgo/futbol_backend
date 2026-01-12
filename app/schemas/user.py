from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class UserBase(BaseModel):
    username:str = None
    email:Optional[EmailStr] = None
    full_name:str = None
    admin:bool = Field(default=False)
    disable:bool = Field(default=False)

class UserCreate (UserBase):  
    pass


class UserUpdate (UserBase):  
    id:int

class UserRead(UserBase):
    id:int