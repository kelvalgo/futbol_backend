from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field

class User_base(SQLModel):
    username:str
    email:EmailStr
    full_name:str
    role:bool
    disable:bool

class User_create (User_base):  
    password:str 

class User_update (User_base):  
    pass 

class User_read(User_base):
    id:int