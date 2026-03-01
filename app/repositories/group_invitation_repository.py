from sqlmodel import Session
from app.core.enums.invitationStatus import InvitationStatus
from app.core.enums.rol import Rol
from app.filter.invitation_filter import InvitationFilter, Invitationsend
from app.models.group_friends import GroupFriends
from app.models.user import User
from sqlmodel import Session,select
from app.models.group_invitation import GroupInvitation
from app.schemas.group_invitation import GroupInvitationRead, GroupInvitationReadSend


def exists_invitation(session: Session,data:GroupInvitation):

    statement=select(GroupInvitation).where(GroupInvitation.id_group==data.id_group,GroupInvitation.invited_user_id==data.invited_user_id,GroupInvitation.status==InvitationStatus.pending)
    
    return session.exec(statement).all()  

def create_inivitation(session: Session,data:GroupInvitation)->GroupInvitation:
    session.add(data)
    return data

def accept_inivitation(session: Session,data:GroupInvitation)->GroupInvitation:
    data.status= InvitationStatus.accepted
    session.add(data)
    return data

def list_invitation(session:Session,status:InvitationStatus,param:InvitationFilter)->GroupInvitationRead:
    statement = (
        select(GroupInvitation, GroupFriends.name,User.username,User.full_name)
        .join(GroupFriends, GroupFriends.id == GroupInvitation.id_group)
        .join(User, User.id == GroupInvitation.invited_by_user_id)
        .where(
            GroupInvitation.status == status,
            GroupInvitation.invited_user_id == param.invited_user_id
        )
        .offset(param.skip)
        .limit(param.limit)
        )
    results=session.exec(statement).all()  
    return [
        GroupInvitationRead(
            id=inv.id,
            status=inv.status,
            invited_by_group_name=invited_by_group_name,   
            invited_by_username=invited_by_username,
            invited_by_userfullname=invited_by_userfullname,
        )
        for inv, invited_by_group_name,invited_by_username,invited_by_userfullname in results
    ]


def list_invitation_send(session:Session,status:InvitationStatus,param:Invitationsend)->GroupInvitationReadSend:
    statement = (
        select(GroupInvitation, GroupFriends.name,User.username,User.full_name)
        .join(GroupFriends, GroupFriends.id == GroupInvitation.id_group)
        .join(User, User.id == GroupInvitation.invited_user_id)
        .where(
            GroupInvitation.status == status,
            GroupInvitation.invited_by_user_id == param.invited_by_user_id
        )
        .offset(param.skip)
        .limit(param.limit)
        )
    results=session.exec(statement).all()  
    return [
        GroupInvitationReadSend(
            id=inv.id,
            status=inv.status,
            invited_by_group_name=invited_by_group_name,   
            invited_username=invited_username,
            invited_userfullname=invited_userfullname,


        )
        for inv, invited_by_group_name,invited_username,invited_userfullname in results
    ]

  
def get_invitation(session:Session,id_invitation:int)->GroupInvitation:
    statement=select(GroupInvitation).where(GroupInvitation.id==id_invitation)
    return session.exec(statement).first()

def rejected_invitation(session: Session,data:GroupInvitation)->GroupInvitation:
    data.status= InvitationStatus.rejected
    session.add(data)
    return data