from pydantic import BaseModel,EmailStr,Field, SecretStr
from typing import Optional

from app.core.enums.status_enum import Status

class UserBase(BaseModel):
    username:str = None
    email:Optional[EmailStr] = None
    full_name:str = None
    status:Status = Field(default=Status.active)

class UserCreate (BaseModel):  
    username:str = None
    email:Optional[EmailStr] = None
    full_name:str = None


class UserUpdatePut (BaseModel):  
    id:int
    username:str
    email:Optional[EmailStr]
    full_name:str 
    #admin:bool 
    status:Status

class UserUpdatePatch (UserBase):  
    id:int    

class UserRead(UserBase):
    id:int

class NewAcount(BaseModel):
    username:str
    full_name:str
    email:Optional[EmailStr] = None 
    password:SecretStr 
