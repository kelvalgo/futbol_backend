from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException, Query,status
from app.core.enum.rol import Rol
from app.core.security.hashing import hash_password
from app.models.group_friends import GroupFriends
from app.models.skill import  Skill
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security.security import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.models.user_groupf import UserGroupF
from app.schemas.user_groupf import UserGroupfCreate
from app.services.user_service import create_relation_user_groupf, list_users_of_group,create_users_by_group
from app.filter.group_filter import GroupFilter
from app.filter.pagination import Pagination


from oso import Oso
from app.auth.oso import get_oso



router=APIRouter(prefix="/user", tags=["User"])



@router.get("/{id_group}/id_group",response_model=list[UserRead],
               status_code=status.HTTP_200_OK)
async def list_user(    
    session: sessionDep,
    param:GroupFilter = Depends(),
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
   
    # Validation 
    if not oso.is_allowed(current_user.id, "user", param.group_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Forbidden"
        )
    
    return list_users_of_group(session,param)



@router.post("/{id_group}/id_group",response_model=UserRead,
               status_code=status.HTTP_201_CREATED)
async def create_user(
    session: sessionDep,
    user_in:UserCreate,
    id_group:int,
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
    ):

     # Validation 
    if not oso.is_allowed(current_user.id, "admin",id_group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Forbidden"
        )

    new_user=create_users_by_group(session,user_in)
    usergf=UserGroupfCreate(
                    user_id=new_user.id,
                    group_id=id_group,
                    rol=Rol.user,
                    disable=False,
                    fecha_ingreso=datetime.now().strftime("%Y-%m-%d")
                    )    
    user_gf = UserGroupF(**usergf.model_dump())
    create_relation_user_groupf(session,user_gf)
    session.commit()
    print(f"por aqui paso {new_user}")
    return new_user