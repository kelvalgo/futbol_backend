from fastapi import APIRouter,Depends,HTTPException,status
from app.auth.context import RequestContext
from app.models.group_friends import GroupFriends
from app.db.db import sessionDep
from app.core.security.security import get_current_user
from app.models.user import User
from app.schemas.group_friends import GroupFriendCreate, GroupFriendRead
from app.schemas.new_password import NewPassword
from app.schemas.user import UserCreate, UserRead,NewAcount
from app.services.groupf_service import create_group_friend
from app.services.user_service import create_new_password,list_users_of_group,create_users_by_group,create_new_acount
from app.filter.group_filter import UserGroupFilter
from app.core.enums.auth_results import AuthResult


from oso import Oso
from app.auth.oso import get_oso



router=APIRouter(prefix="/user", tags=["User"])



@router.get("/id_group/{id_group}/",response_model=list[UserRead],
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
    context=RequestContext(current_user, session)
    
    if not oso.is_allowed(context, "read", group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    return list_users_of_group(session,group_id,param)



@router.post("/id_group/{id_group}/",
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
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"write",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )

    message=create_users_by_group(session,user_in,id_group)
    return message


@router.post("/change-password",
            status_code=status.HTTP_200_OK)
async def new_password(
    data:NewPassword,
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):  
  
  """
    new password.

    **Permissions**
    - User logged.

    **Parameters**
    - **data**: new_password.

    **Returns**
    - The user.
  """
  message=create_new_password(session,current_user,data) 
  return message


@router.post("/new_count",
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
        message=create_new_acount(session,data)
        return message
