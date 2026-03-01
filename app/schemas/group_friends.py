from pydantic import BaseModel,Field 
from typing import Optional
from app.core.enums.status_enum import Status
from app.core.enums.rol import Rol

class GroupFriendsBase(BaseModel):
    name:str=Field(description="name group")
    description:str =Field(description="description group", default=None)
   

class GroupFriendCreate(GroupFriendsBase):        
    pass

class GroupFriendUpdatePut(GroupFriendsBase):
    id:int
    last_date_donation: Optional[str] = None
    perioding_donation:int = Field(default=30)  # días
    is_active: Status = Field(default=Status.active)

class GroupFriendUpdatePatch(GroupFriendsBase):
    id:int
    last_date_donation: Optional[str] = None
    perioding_donation:int = Field(default=30)  # días
    is_active: Status = Field(default=Status.active)

class GroupFriendReadDonation(GroupFriendsBase):
    id:int
    last_date_donation: Optional[str] = None
    perioding_donation:int = Field(default=30)  # días
    is_active: Status = Field(default=Status.active)    
    date_creation:str | None =None

class GroupFriendRead(GroupFriendsBase):
    group_id:int    
    group_is_active: Status = Field(default=Status.active)    
    date_creation:str | None =None
    user_rol:Rol
    user_disable:bool
