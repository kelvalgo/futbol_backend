
from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session
from fastapi import HTTPException,status
from app.schemas.user_groupf import UserGroupfCreate
from app.services.user_groupf_service import create_usergroupf
from app.core.enums.invitationStatus import InvitationStatus
from app.filter.invitation_filter import InvitationFilter, Invitationsend
from app.models.group_invitation import GroupInvitation
from app.repositories.group_invitation_repository import exists_invitation, create_inivitation, list_invitation, list_invitation_send, rejected_invitation
from app.schemas.group_invitation import GroupInvitationCreate, GroupInvitationRead
from app.repositories.group_invitation_repository import  get_invitation, accept_inivitation
from sqlalchemy.exc import SQLAlchemyError
from app.core.enums.rol import Rol

def get_invitations(session:Session,id_invitation:int)->GroupInvitation:

    return get_invitation(session,id_invitation)


def create_invitations(session: Session,data:GroupInvitationCreate,id_group:int):
    
    
    invitation=GroupInvitation(**data.model_dump())
    invitation.id_group=id_group
    invitation.status=InvitationStatus.pending

    if exists_invitation(session,invitation):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A pending invitation already exists for this user in this group."
        )
    
    create_inivitation(session,invitation)     
    session.commit()
    return {"message": "invitation created successfully"}


def get_list_invitacion(session:Session,status:InvitationStatus,current_user:int)->list[GroupInvitationRead]:
        param=InvitationFilter(invited_user_id=current_user)
        return list_invitation(session,status,param)

def get_list_invitacion_send(session:Session,status:InvitationStatus,current_user:int)->list[GroupInvitationRead]:
        param=Invitationsend(invited_by_user_id=current_user)
        return list_invitation(session,status,param)
        
def reject_invitations(session:Session,id_invitation:int):

    invitationg=get_invitation(session,id_invitation)
    if  invitationg:

        rejected_invitation(session,invitationg)
        session.commit()

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This invitation not exists"
        )        
   
    

    return {"message": "Invitation reject successfully"}        

def accept_invitations(session:Session,id_invitation:int): 
    

    try:
        invitationg=get_invitation(session,id_invitation)
        usergroupf=UserGroupfCreate(user_id=invitationg.invited_user_id,
                         group_id=invitationg.id_group,
                         rol=Rol.user,
                         disable=False,
                         date_creation= datetime.now().strftime("%Y-%m-%d"))

        accept_inivitation(session,invitationg)
        create_usergroupf(session,usergroupf)
        session.commit()
        return  {"message": "Invitation accept successfully"}        

    except SQLAlchemyError:
        session.rollback()
    return False
    