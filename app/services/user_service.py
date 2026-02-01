from fastapi import HTTPException
from sqlalchemy import select
from sqlmodel import Session
from app.core.security.hashing import hash_password
from app.models.user import User
from app.models.user_groupf import UserGroupF
from app.repositories.user_repository import create_user, create_user_groupf, get_user_by_username, get_users_by_group
from app.filter.group_filter import GroupFilter
from app.schemas.user import UserCreate
from fastapi import HTTPException,status


def list_users_of_group(
    session: Session,
    param: GroupFilter,
    ):   
    
    return get_users_by_group(session, param) 


def create_users_by_group(
    session: Session,
    user_in: UserCreate,
) -> User:

    existing_user = get_user_by_username(session, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    user_new = User(**user_in.model_dump())
    user_new.hashed_password = hash_password("Inicio")  
    
    return  create_user(session,user_new)

def create_relation_user_groupf(session: Session,user_group:UserGroupF)->None:
     create_user_groupf(session,user_group)

   
    