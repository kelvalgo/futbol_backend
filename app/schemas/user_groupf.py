from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from app.core.enums.rol import Rol

class UserGroupf(BaseModel):
    user_id:int
    group_id:int
    rol:Rol
    disable:bool
    date_creation:str

class UserGroupfCreate (UserGroupf):      
    pass


class UserGroupfUpdatePut (BaseModel): 
    pass

class UserGroupfUpdatePatch (BaseModel):  
   rol: Optional[Rol]= None
   disable:Optional[bool]= None    

class UserGroupfRead(UserGroupf):
    id:int

class UserWithGroupRead(BaseModel):
    user_id: int
    user_name: str
    user_full_name:str
    


 
                
       
                       