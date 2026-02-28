from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from app.core.enums.invitationStatus import InvitationStatus
from app.core.enums.status_enum import Status

class GroupInvitation(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_group: int
    invited_user_id: int
    invited_by_user_id: int
    status: InvitationStatus