from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session
from app.core.enums.rol import Rol
from app.models.user_groupf import UserGroupF
from app.repositories.groupf_repository import create_group, get_group_of_admin
from app.repositories.user_repository import create_user_groupf
from app.schemas.group_friends import GroupFriendCreate
from fastapi import HTTPException,status
from app.models.group_friends import GroupFriends
from app.schemas.user_groupf import UserGroupfCreate

def create_group_friend(session:Session, data: GroupFriendCreate,user_id:int)->GroupFriends:
    groups=get_group_of_admin(session,user_id)
    if len(groups)>2:
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
    print(f"Antes de UserGroupf {user_group}")
    user_gf = UserGroupF(**user_group.model_dump())
    print(f"dato {user_gf}")
    create_user_groupf(session,user_gf)   
    session.commit()

    return group



