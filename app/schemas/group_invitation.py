from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
from app.core.enums.invitationStatus import InvitationStatus
from app.core.enums.status_enum import Status

class GroupInvitation(BaseModel):
    invited_user_id: int

class GroupInvitationCreate(BaseModel):
    invited_user_id: int
    invited_by_user_id: int
    InvitationStatus.pending

class GroupInvitationRead(BaseModel):    
    id: int 
    status: InvitationStatus
    group_name: str