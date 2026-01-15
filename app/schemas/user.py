from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class UserBase(BaseModel):
    username:str = None
    email:Optional[EmailStr] = None
    full_name:str = None
    admin:bool | None = Field(default=False)
    disable:bool  | None = Field(default=False)

class UserCreate (UserBase):  
    pass


class UserUpdatePut (BaseModel):  
    id:int
    username:str
    email:Optional[EmailStr]
    full_name:str 
    admin:bool 
    disable:bool

class UserUpdatePatch (UserBase):  
    id:int    

class UserRead(UserBase):
    id:int