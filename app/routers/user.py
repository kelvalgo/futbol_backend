from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException, Query,status
from pydantic import SecretStr
from app.core.enums.rol import Rol
from app.core.security.hashing import hash_password
from app.models.group_friends import GroupFriends
from app.models.skill import  Skill
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security.security import get_current_user
from app.models.user import User
from app.schemas.group_friends import GroupFriendCreate, GroupFriendRead
from app.schemas.user import UserCreate, UserRead
from app.models.user_groupf import UserGroupF
from app.services.groupf_service import create_group_friend
from app.services.user_service import create_new_password, create_relation_user_groupf, list_users_of_group,create_users_by_group,create_new_acount
from app.filter.group_filter import UserGroupFilter
from app.filter.pagination import Pagination
from app.schemas.new_acount import NewAcount
from app.core.enums.auth_results import AuthResult


from oso import Oso
from app.auth.oso import get_oso



router=APIRouter(prefix="/user", tags=["User"])



@router.get("/group/{id_group}/",response_model=list[UserRead],
               status_code=status.HTTP_200_OK)
async def list_user(    
    session: sessionDep,
    group_id: int,
    param:UserGroupFilter = Depends(),
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    """
    List users.

    **Permissions**
    - User logged.

    **Parameters**
    - **active**: Show users active or unactivate
    - **group_id**: Identifier of the group.

    **Returns**
    - List of users in the group.
    """
    # Validation 
    group = GroupFriends(id=group_id)
    
    if not oso.is_allowed(current_user, "read", group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    return list_users_of_group(session,group_id,param)



@router.post("/{id_group}/id_group",response_model=UserRead,
               status_code=status.HTTP_201_CREATED)
async def create_user(
    session: sessionDep,
    user_in:UserCreate,
    id_group:int,
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
    ):

    """
    Create a user in a group.

    **Permissions**
    - Only administrators can create users in a group.

    **Parameters**
    - **id_group**: Identifier of the group.
    - **user_in**: User data to be created.

    **Returns**
    - The newly created user.
    """

     # Validation 
    group = GroupFriends(id=id_group)
    if not oso.is_allowed(current_user,"write",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )

    new_user=create_users_by_group(session,user_in,id_group)
    return new_user


@router.put("/new_password",
            response_model=UserRead,
            status_code=status.HTTP_200_OK)
async def new_password(
    new_pass:SecretStr,
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):  
  
  """
    new password.

    **Permissions**
    - User logged.

    **Parameters**
    - **new_pass**: new password.

    **Returns**
    - The user.
  """
  user=create_new_password(session,current_user,new_pass) 
  return user

@router.post("/new_count",response_model=UserRead,
             status_code=status.HTTP_201_CREATED)
async def new_account(session: sessionDep, data:NewAcount):
        
        """
        new account.

        **Permissions**
        - Unpermissions.

        **Parameters**
        - **NewCount**: new acount.

        **Returns**
        - The newly account.
        """
        count=create_new_acount(session,data)
        return count


@router.post("/new_group",response_model=GroupFriendRead,
             status_code=status.HTTP_201_CREATED)
async def new_group(session: sessionDep, data:GroupFriendCreate,
                    current_user: User = Depends(get_current_user)):
      
        """
        new group.

        **Permissions**
        - User logged.

        **Parameters**
        - **data**: Group.

        **Returns**
        - The newly group..
        """
        new_group=create_group_friend(session,data)
        
        return new_group