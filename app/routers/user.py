from fastapi import APIRouter,Depends,HTTPException,status
from app.auth.context import RequestContext
from app.db.db import sessionDep
from app.core.security.security import get_current_user
from app.models.user import User
from app.schemas.new_password import NewPassword
from app.schemas.user import UserCreate, UserRead,NewAcount
from app.schemas.user_groupf import UserWithGroupRead
from app.services.user_service import create_new_password, list_users,list_users_of_group,create_users_by_group,create_new_acount
from app.filter.group_filter import Group
from app.filter.user_group_filter import UserGroupFilter
from app.core.enums.auth_results import AuthResult


from oso import Oso
from app.auth.oso import get_oso



router=APIRouter(prefix="/user", tags=["User"])



@router.get("/me/id_group/{id_group}/",response_model=list[UserRead],
               status_code=status.HTTP_200_OK)
async def list_user_group(    
    session: sessionDep,
    id_group: int,
    param:UserGroupFilter = Depends(),
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    """
    Retrieve users belonging to a specific group.

    Returns a paginated list of users associated with the given group.
    Results can be filtered by membership status.

    **Permissions**
    - Authenticated users only.
    - Requires "read" permission on the target group (validated via Oso).

    **Path Parameters**
    - **group_id** (int): Unique identifier of the group.

    **Query Parameters**
    - **status** (str): Filter users by membership status ("active" or "inactive").
    - Pagination parameters inherited from Pagination schema.

    **Responses**
    - 200: List of users successfully retrieved.
    - 403: Not authorized to access this group.
    - 404: Group not found.
    - 422: Validation error.
    """
    # Validation 
    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    
    if not oso.is_allowed(context, "list_user_group", group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    return list_users_of_group(session,id_group,param)


@router.get("/id_group/{id_group}/internal",response_model=list[UserWithGroupRead],
               status_code=status.HTTP_200_OK)
async def list_user(    
    session: sessionDep,
    id_group: int,
    param:UserGroupFilter = Depends(),
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    """
    Retrieve the internal list of users associated with groups 
    other than the specified group.

    Returns a paginated list of active users along with their 
    associated group name, excluding the provided group ID.

    **Permissions**
    - Authenticated users only.
    - Requires "read_all_users" permission on the target group (validated via Oso).

    **Path Parameters**
    - **id_group** (int): Identifier of the group to be excluded from the results.

    **Query Parameters**
    - Pagination parameters provided via UserGroupFilter.

    **Responses**
    - 200: Internal user list successfully retrieved.
    - 403: Not authorized to access internal group data.
    - 404: Group not found.
    - 422: Validation error.
    """

    # Validation 
    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    
    if not oso.is_allowed(context, "read_all_users", group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    return list_users(session,id_group,param)




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
    Create a new user within a specific group.

    This endpoint allows an authorized administrator to create a user
    and associate them with the specified group.

    **Permissions**
    - Authenticated users only.
    - Requires "write" permission on the target group (validated via Oso).

    **Path Parameters**
    - **id_group** (int): Unique identifier of the group.

    **Request Body**
    - **username** (str, optional): Username of the new user.
    - **email** (EmailStr, optional): Email address of the user.
    - **full_name** (str, optional): Full name of the user.

    **Responses**
    - 201: User successfully created and added to the group.
    - 403: Not authorized to create users in this group.
    - 404: Group not found.
    - 422: Validation error.
    """

     # Validation 
    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"create_user",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )

    message=create_users_by_group(session,user_in,id_group)
    return message


@router.post("/me/change-password",
            status_code=status.HTTP_200_OK)
async def change_password(
    data:NewPassword,
    session: sessionDep,
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):  
  
  """
    Change the current user's password.

    Allows an authenticated user to update their password by providing
    their current password and a new one.

    **Permissions**
    - Authenticated users only.

    **Request Body**
    - **current_password** (SecretStr): User's current password.
    - **new_password** (SecretStr): New password to replace the current one.

    **Responses**
    - 200: Password updated successfully.
    - 400: Current password is incorrect.
    - 401: Not authenticated.
    - 422: Validation error.
    """
  context=RequestContext(current_user, session)
  if not oso.is_allowed(context,"change_password",context):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )

 
  message=create_new_password(session,current_user,data) 
  return message


@router.post("/new_count",
             status_code=status.HTTP_201_CREATED)
async def new_account(session: sessionDep, data:NewAcount):
        
        """
        Create a new user account.

        Registers a new user in the system with authentication credentials.

        **Permissions**
        - Public endpoint (no authentication required).

        **Request Body**
        - **username** (str): Unique username for the account.
        - **full_name** (str): Full name of the user.
        - **email** (EmailStr, optional): Valid email address.
        - **password** (SecretStr): User password (stored securely as a hash).

        **Responses**
        - 201: User account created successfully.
        - 400: Username or email already exists.
        - 422: Validation error.
        """
        message=create_new_acount(session,data)
        return message

