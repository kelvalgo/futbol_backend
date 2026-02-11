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

class UserGroupfUpdatePatch (UserGroupf):  
    id:int    

class UserGroupfRead(UserGroupf):
    id:int