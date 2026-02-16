from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlmodel import Session
from app.core.enums.rol import Rol
from app.core.security.hashing import hash_password
from app.models.user import User
from app.models.user_groupf import UserGroupF
from app.repositories.user_repository import create_acount, create_user, create_user_groupf, get_user_by_username, get_users_by_group, new_password
from app.filter.group_filter import UserGroupFilter
from app.routers.auth import autenticate_user
from app.schemas.new_password import NewPassword
from app.schemas.user import UserCreate,NewAcount
from fastapi import HTTPException,status
from app.core.enums.status_enum import Status
from app.schemas.user_groupf import UserGroupfCreate


def list_users_of_group(
    session: Session,
    group_id:int,
    param: UserGroupFilter,
    ):   
    
    return get_users_by_group(session,group_id,param) 


def create_users_by_group(
    session: Session,
    user_in: UserCreate,
    id_group:int,
):

    existing_user = get_user_by_username(session, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    new_user=User(
         username=user_in.username,
         full_name=user_in.full_name,
         email=user_in.email,
         status=Status.active            
        )    
    
    new_user.hashed_password = hash_password(user_in.username)  

    new_user=create_user(session,new_user)
    session.flush()
    usergf=UserGroupfCreate(
                    user_id=new_user.id,
                    group_id=id_group,
                    rol=Rol.user,
                    disable=False,
                    date_creation=datetime.now().strftime("%Y-%m-%d")
                    )    
    user_gf = UserGroupF(**usergf.model_dump())
    print(f"dato: {user_gf}")
    create_relation_user_groupf(session,user_gf)
    session.commit()
    return  {"message": "User created successfully"}

def create_relation_user_groupf(session: Session,user_group:UserGroupF)->None:
     create_user_groupf(session,user_group)


def create_new_acount(session: Session,new_count:NewAcount):

    count = session.exec(
            select(User).where(User.username == new_count.username)
        ).first()

    if not count:
            
            hashed_password=hash_password(new_count.password.get_secret_value())

            count = User(username=new_count.username,full_name=new_count.full_name,
                         email=new_count.email,hashed_password=hashed_password)
            create_acount(session,count)
            session.commit()

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )        

    return {"message": "Acount created successfully"}
  
def create_new_password(session:Session,user:User,data:NewPassword):
    if not autenticate_user(user.username,data.current_password.get_secret_value(),session):
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    new_password(session,user,data.new_password.get_secret_value())
    session.commit()
    return {"message": "Password updated successfully"}