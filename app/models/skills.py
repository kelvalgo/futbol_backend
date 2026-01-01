from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field

class Player_base(SQLModel):
    name:str
    position:str
    spatial_condition:bool

class Player_create (Player_base):  
    pass 

class Player_update (Player_base):  
    pass 

class User(Player_base,table=True):
    id:int|None=Field(default=None,primary_key=True)