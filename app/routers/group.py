from fastapi import APIRouter,Depends, HTTPException, Query,status
from app.core.enums.auth_results import AuthResult
from app.filter.user_filter import UserFilter
from app.db.db import sessionDep
from app.core.security.security import get_current_user
from app.models.user import User
from app.schemas.group_friends import GroupFriendCreate, GroupFriendRead
from app.services.groupf_service import create_group_friend, list_groups
from app.filter.pagination import Pagination
from app.auth.context import RequestContext
from oso import Oso
from app.auth.oso import get_oso



router=APIRouter(prefix="/group", tags=["Group"])



@router.post("/me/new_group",
             status_code=status.HTTP_201_CREATED)
async def new_group(session: sessionDep,
                    data:GroupFriendCreate,   
                    current_user: User = Depends(get_current_user),
                    oso:Oso=Depends(get_oso)
                    ):
      
        """
        Create a new group of friends.

        Allows an authenticated user to create a new friends group.

        **Permissions**
        - The user must be authenticated (logged in).

        **Parameters**
        - **data**: `GroupFriendCreate` object containing the name and description for the new group.
            - `name`: Name of the group (string).
            - `description`: Optional description for the group (string).

        **Returns**
        - A confirmation message and the details of the newly created group.
        """
        
        context=RequestContext(current_user, session)
        if not oso.is_allowed(context,"new_group",context):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail=AuthResult.FORBIDDEN.value
                )
        
        
        message=create_group_friend(session,data,current_user.id)
        
        return message


@router.get("/me/list_group/",response_model=list[GroupFriendRead],
               status_code=status.HTTP_200_OK)
async def get_list_groups(    
    session: sessionDep,
    group_disable:bool= Query(False, description="Filter groups by disable status"),   
    param:Pagination= Depends(),
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    """
    Retrieves a paginated list of groups associated with the authenticated user.

    This endpoint returns the groups linked to the current user, with optional
    filtering based on the group's disabled status.

    **Features:**
    - Pagination support using skip and limit parameters.
    - Optional filtering by disabled status.
    - Requires authenticated user.

    **Query Parameters:**
    - group_disable (bool, optional): If True, returns only disabled groups.
    If False (default), returns active groups.

    **Authentication:**
    - Requires a valid authenticated user session.

    **Returns:**
    - A list of groups associated with the current user.

    **Response Model:**
    - List[GroupFriendRead]

    **Raises:**
    - 401 Unauthorized: If the user is not authenticated.
    - 400 Bad Request: If pagination parameters are invalid.
    """
    
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"get_list_groups",context):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=AuthResult.FORBIDDEN.value
            )
        
    
    
    userf=UserFilter(skip=param.skip,limit=param.limit,user_id=current_user.id)        
    return list_groups(session,userf,group_disable)





