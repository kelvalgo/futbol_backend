from datetime import datetime
from pydantic import SecretStr
from sqlalchemy import exists
from sqlmodel import Session,select
from app.schemas.user import UserRead
from app.core.enums.rol import Rol
from app.core.security.hashing import hash_password
from app.models.group_friends import GroupFriends
from app.models.user import User
from app.models.user_groupf import UserGroupF
from app.filter.user_group_filter import UserGroupFilter
from app.schemas.user_groupf import UserWithGroupRead


def get_users_by_group(session:Session,group_id:int,param:UserGroupFilter):

    statement=(select(
           User.id,User.username,User.full_name,User.email,UserGroupF.rol,User.status,UserGroupF.disable)
            .join(UserGroupF,UserGroupF.user_id==User.id)
            .where(UserGroupF.group_id==group_id,UserGroupF.disable==param.disabled)
            .offset(param.skip).limit(param.limit)
        )
        
    return session.exec(statement).all()  

def get_users(session:Session,group_id:int,param:UserGroupFilter):  

    
         
    subquery = (
    select(1)
    .where(
        UserGroupF.user_id == User.id,
        UserGroupF.group_id == group_id,
        UserGroupF.disable == False
    )
    .correlate(User)   # 👈 CLAVE
    )


    statement = (
    select(
        User.id,
        User.username,
        User.full_name
    )
    .where(~exists(subquery))
    .order_by(User.username)
    .offset(param.skip)
    .limit(param.limit)
    )
  
    '''  
    statement = (
        select(User.id, User.username,User.full_name, GroupFriends.name.label("group_name"),UserGroupF.disable.label("user_disable_group"),
               UserGroupF.rol.label("user_rol"))
        .join(UserGroupF, UserGroupF.user_id == User.id)
        .join(GroupFriends, GroupFriends.id == UserGroupF.group_id)
        .where(GroupFriends.id != group_id,UserGroupF.disable==param.disabled)
        ).order_by(GroupFriends.name) .offset(param.skip).limit(param.limit)
    '''

    users = session.exec(statement).all() 
    return  users

def get_user_by_username(session: Session, username: str) -> User | None:

    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def create_user(session: Session, user: User) -> User:
        
        session.add(user)
        return user
    



def create_acount(session:Session,new_count:User)->User: 
        
        session.add(new_count)
        return new_count
    
def new_password(session:Session,user:User,new_pass:str)->User:
        new_hash = hash_password(new_pass)
        user.hashed_password = new_hash

        session.add(user)             
        return user

