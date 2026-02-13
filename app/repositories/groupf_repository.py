from sqlmodel import Session
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
    