from sqlmodel import Session
from app.filter.user_filter import UserFilter
from app.models.user import User
from app.core.enums.rol import Rol
from app.models.group_friends import GroupFriends
from app.models.user_groupf import UserGroupF
from sqlmodel import Session,select




def create_group(session:Session,param:GroupFriends):
    session.add(param)
    session.flush()
    session.refresh(param)
    return param
    

def get_group_of_admin(session:Session,id_user:int)->list[UserGroupF]:
    
    statement=select(UserGroupF).where(UserGroupF.user_id==id_user,UserGroupF.rol==Rol.admin)
    
    return session.exec(statement).all()

def get_list_groups(session:Session,param:UserFilter,group_disable:bool):
    statement=select(GroupFriends.id,GroupFriends.name,GroupFriends.description,GroupFriends.date_creation,GroupFriends.is_active,UserGroupF.rol,UserGroupF.disable).join(UserGroupF, GroupFriends.id == UserGroupF.group_id
            ).where(UserGroupF.disable==group_disable,UserGroupF.user_id==param.user_id
            ).order_by(GroupFriends.name) .offset(param.skip).limit(param.limit)
    groups=session.exec(statement).all()

    return groups
    
    