from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session
from app.core.enums.rol import Rol
from app.filter.user_filter import UserFilter
from app.models.user_groupf import UserGroupF
from app.models.user import User
from app.repositories.groupf_repository import create_group, get_group_of_admin, get_list_groups
from app.repositories.user_groupf_repositoy import create_user_groupf
from app.schemas.group_friends import GroupFriendCreate, GroupFriendRead
from fastapi import HTTPException,status
from app.models.group_friends import GroupFriends
from app.schemas.user_groupf import UserGroupfCreate
from app.core.config import settings

def create_group_friend(session:Session, data: GroupFriendCreate,user_id:int)->GroupFriends:
    groups=get_group_of_admin(session,user_id)
    if len(groups)>settings.LIMIT_GROUPS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="exceeds the limit of groups"
        )
    
    new_group=GroupFriends(
                    name=data.name,
                    description=data.description,
                    date_creation=datetime.now().strftime("%Y-%m-%d")
                    )    
    
    group=create_group(session,new_group)
    user_group=UserGroupfCreate(
                    user_id=user_id,
                    group_id=group.id,
                    rol=Rol.admin,
                    disable=False,
                    date_creation=new_group.date_creation

    )
    user_gf = UserGroupF(**user_group.model_dump())
    create_user_groupf(session,user_gf)   
    session.commit()

    return {"message": "Acount created successfully"}


def list_groups(session:Session,userf:UserFilter,group_disable:bool):

    list_groups=get_list_groups(session,userf,group_disable)
    groups_response = [GroupFriendRead(id=g.id, name=g.name,description=g.description,date_creation=g.date_creation,is_active=g.is_active) for g in list_groups]
 
    return groups_response
    


