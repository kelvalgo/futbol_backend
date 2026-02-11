from pydantic import BaseModel,Field 
from typing import Optional
from app.core.enums.status_enum import Status

class GroupFriendsBase(BaseModel):
    user_id:int
    name:str=Field(description="name group")
    description:str =Field(description="description group", default=None)
    last_date_donation: Optional[str] = None
    perioding_donation:int = Field(default=30)  # días
    is_active: Status = Field(default=Status.active)

class GroupFriendCreate(GroupFriendsBase):    
    date_creation:str=None
    pass

class GroupFriendUpdatePut(GroupFriendsBase):
    pass

class GroupFriendUpdatePatch(GroupFriendsBase):
    pass

class GroupFriendRead(GroupFriendsBase):
    id:int
    pass
