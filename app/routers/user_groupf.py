from fastapi import APIRouter,Depends,HTTPException,status
from app.services.user_groupf_service import update_usergroupf_service
from app.schemas.user_groupf import UserGroupfUpdatePatch
from app.filter.group_filter import Group
from app.core.enums.auth_results import AuthResult
from app.db.db import sessionDep
from app.core.security.security import get_current_user
from app.models.user import User
from app.auth.context import RequestContext
from oso import Oso
from app.auth.oso import get_oso


router=APIRouter(prefix="/user_groupf", tags=["UserGroupf"])

@router.patch("/groups/{group_id}/users/{user_id}/internal",
    status_code=status.HTTP_200_OK
)

def update_usergroupf(session: sessionDep,
                 group_id: int,
                 user_id: int,
                 users_groupf:UserGroupfUpdatePatch,
                 current_user: User = Depends(get_current_user),
                 oso:Oso=Depends(get_oso)): 
    
    """
    Update internal user-group relationship settings.

    This endpoint allows an authorized user to partially update internal attributes
    of a specific user's membership within a group.

    The operation is restricted by authorization policies enforced through Oso.
    The requesting user must have permission to perform the "update_usergroupf"
    action on the specified group.

    Path Parameters:
    - group_id (int): Identifier of the target group.
    - user_id (int): Identifier of the user whose group membership will be updated.

    Request Body:
    - users_groupf (UserGroupfUpdatePatch): Partial update payload containing
    the fields to be modified in the user-group relationship.

    Authorization:
    - Requires authenticated user.
    - Requires proper permissions validated by Oso policies.

    Responses:
    - 200 OK: The user-group relationship was successfully updated.
    - 403 Forbidden: The user does not have permission to update this group membership.
    - 404 Not Found: The specified group or user membership does not exist.
    """
    
    group = Group(id_group=group_id)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"update_usergroupf",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    data=(group_id,user_id)
    return update_usergroupf_service(session,data,users_groupf)