from sqlmodel import Session,select
from app.models.user import User
from app.models.user_groupf import UserGroupF


def get_users_by_group(session:Session,id_group:int)->list[User]:
    
    statement=select(User).join(UserGroupF,UserGroupF.user_id==User.id).where(UserGroupF.group_id==id_group)
    
    return session.exec(statement).all()