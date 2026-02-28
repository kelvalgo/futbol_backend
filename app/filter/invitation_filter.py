from app.filter.pagination import Pagination
from pydantic import BaseModel

class InvitationFilter(Pagination):
    invited_user_id:int

class Invitation(BaseModel):
    invitation_id:int 
    invited_user_id:int   

class Invitationsend(Pagination):
    invited_by_user_id:int    