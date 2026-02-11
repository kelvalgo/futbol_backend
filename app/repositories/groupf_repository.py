from sqlmodel import Session
from app.core.enums.rol import Rol
from app.models.user_groupf import UserGroupF
from sqlmodel import Session,select




def create_group(session:Session,param:UserGroupF):
    session.add(param)
    session.flush()
    session.refresh(param)
    return param
    

def get_group_of_admin(session:Session,param:int)->list[UserGroupF]:
    
    statement=select(UserGroupF).where(UserGroupF.user_id==param,UserGroupF.rol==Rol.admin)
    
    return session.exec(statement).all()
    