from datetime import datetime
from sqlmodel import Session,select
from app.core.enum.rol import Rol
from app.models.user import User
from app.models.user_groupf import UserGroupF
from app.filter.group_filter import GroupFilter







def get_users_by_group(session:Session,param:GroupFilter)->list[User]:
    
    statement=select(User).join(UserGroupF,UserGroupF.user_id==User.id).where(UserGroupF.group_id==param.group_id).offset(param.skip).limit(param.limit)
    
    return session.exec(statement).all()


def get_user_by_username(session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.flush()
    session.refresh(user)
    return user

def create_user_groupf(session: Session,user_group:UserGroupF):   
    session.add(user_group)
    session.flush()
    return


