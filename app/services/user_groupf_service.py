from datetime import datetime
from app.filter.user_group_filter import UserGroupFilter
from app.core.enums.rol import Rol
from app.models.user_groupf import UserGroupF
from sqlmodel import Session
from app.repositories.user_groupf_repositoy import create_user_groupf, get_my_membership_repository,update_usergroupf
from app.schemas.user_groupf import UserGroupfCreate, UserGroupfUpdatePatch
from app.core.enums.rol import Rol
from sqlalchemy.exc import SQLAlchemyError
from app.models.group_invitation import GroupInvitation
from fastapi import HTTPException,status




    

def create_usergroupf(session:Session,usergrup:UserGroupfCreate)->bool:   

    user_group=UserGroupfCreate(user_id=usergrup.user_id,
    group_id=usergrup.group_id,
    rol=Rol.user,
    disable=False,
    date_creation= datetime.now().strftime("%Y-%m-%d"))
       
    try:       
        user_gf = UserGroupF(**user_group.model_dump())
        create_user_groupf(session,user_gf)
        session.commit()  
        return True
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

def  update_usergroupf_service(session:Session,data: tuple,param:UserGroupfUpdatePatch):
    try:
        update_usergroupf(session,data,param)
        session.commit()
        return  {"message": "user update successfully"}  
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        ) 
    


def get_my_membership_service(session:Session,group_id:int,user_id:int):

    membership =get_my_membership_repository(session,group_id,user_id)
    print(f"membership: {membership}")

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not in group"
        )
    print(f"membership service: {membership}")    
    return membership

 