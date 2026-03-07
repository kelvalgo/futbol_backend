from datetime import datetime

from sqlmodel import select
from app.core.enums.invitationStatus import InvitationStatus
from app.auth.context import RequestContext
from app.core.enums.rol import Rol
from app.models.user import User
from app.models.group_invitation import GroupInvitation
from app.models.user_groupf import UserGroupF
from app.core.enums.status_enum import Status
from app.filter.group_filter import Group
from app.filter.invitation_filter import Invitation
from app.models.season import Season

def is_member_of_group(ctx: RequestContext, groupf: Group) -> bool:
     session=ctx.db
     try:
            statement = select(UserGroupF).where(
                UserGroupF.user_id == ctx.user.id,
                UserGroupF.group_id == groupf.id_group,
            )
           
            result = session.exec(statement).first()
            
            return result is not None 
     except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False
         
def is_admin_of_group(ctx: RequestContext, groupf: Group) -> bool:
    session=ctx.db
    try:
            statement = select(UserGroupF).where(
                UserGroupF.user_id ==  ctx.user.id,
                UserGroupF.group_id == groupf.id_group,
                UserGroupF.rol==Rol.admin
            )
           
            result = session.exec(statement).first()
            print(result)
            return result is not None 
    except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False 


    '''
    with Session(engine) as session:
        try:
            statement = select(UserGroupF).where(
                UserGroupF.user_id ==  user.id,
                UserGroupF.group_id == groupf.id,
                UserGroupF.rol==Rol.admin
            )
           
            result = session.exec(statement).first()
            print(result)
            return result is not None 
        except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False 
    '''              

def is_user_active(ctx: RequestContext) -> bool:  
    session=ctx.db
    try:
            statement=select(User.status).where(
            User.id==ctx.user.id
            )
            status=session.exec(statement).first()
            return status==Status.active
    except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False
 
    
def has_pending_invitation(ctx:RequestContext, invitation:Invitation) -> bool:
    session=ctx.db
    try:
            statement=select(GroupInvitation.status).where(
            GroupInvitation.id==invitation.invitation_id,GroupInvitation.invited_user_id==invitation.invited_user_id,
            GroupInvitation.status==InvitationStatus.pending
            )
            status=session.exec(statement).first()
            return status==InvitationStatus.pending
    except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False

def has_activate_season (ctx:RequestContext, groupf: Group) -> bool:  
        session=ctx.db

        try:
            statement = select(Season.id).where(
                Season.group_id == groupf.id_group,
                Season.is_active == Status.active
            )

            season = session.exec(statement).first()
            if season:
                  return False
            #True  -> no hay temporada activa -> permitir
            #False -> hay temporada activa -> bloquear
            return season is None

        except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False
        

def has_season (ctx:RequestContext, groupf: Group) -> bool:  
        session=ctx.db

        try:
            statement = select(Season.id).where(
                Season.group_id == groupf.id_group
            )

            season = session.exec(statement).first()
            if season:
                  return False
            #True  -> no hay temporada activa -> permitir
            #False -> hay temporada activa -> bloquear
            return season is None

        except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False        
       