from datetime import datetime
from app.core.enums.rol import Rol
from app.models.user_groupf import UserGroupF
from sqlmodel import Session
from app.repositories.user_groupf_repositoy import create_user_groupf
from app.schemas.user_groupf import UserGroupfCreate
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
    return False

 