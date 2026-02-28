
from app.filter.invitation_filter import Invitation
from fastapi import Query
from app.filter.group_filter import Group
from app.auth.context import RequestContext
from app.core.enums.auth_results import AuthResult
from app.core.enums.invitationStatus import InvitationStatus
from app.core.security.security import get_current_user
from app.db.db import sessionDep
from fastapi import APIRouter,Depends,HTTPException, status
from fastapi import APIRouter
from oso import Oso
from app.auth.oso import get_oso
from app.models.user import User
from app.schemas.group_invitation import GroupInvitation, GroupInvitationCreate, GroupInvitationRead
from app.services.group_invitation_service import accept_invitations, create_invitations, get_list_invitacion, get_list_invitacion_send, reject_invitations
import oso


router=APIRouter(prefix="/invitations", tags=["Invitations"])

@router.post("/id_group/{id_group}/internal",
             status_code=status.HTTP_201_CREATED)
async def create_invitation(session: sessionDep,
                      data:GroupInvitation,
                      id_group:int,
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)):
    """
    Create a group invitation.

    Creates a new pending invitation for a user to join a specific group.

    **Permissions**
    - Only users with write permission on the group can create invitations.

    **Path Parameters**
    - **id_group**: Identifier of the group.

    **Body Parameters**
    - **invited_user_id**: Identifier of the user to be invited.

    **Returns**
    - The created invitation with status set to "pending".
    """
    # Validation 
    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"create_invitation",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    

    invitation=GroupInvitationCreate(invited_user_id= data.invited_user_id,invited_by_user_id=current_user.id)
    message=create_invitations(session,invitation,id_group)
    return message



@router.get("/list_invitation/received",response_model=list[GroupInvitationRead],
               status_code=status.HTTP_200_OK)
async def list_invitation_received(    
    session: sessionDep,
    current_user: User = Depends(get_current_user),
    status:InvitationStatus=Query()
    ):
    """
    List pending,rejected,accepted invitations received for the current user.

    Retrieves all pending,rejected,accepted group invitations where the authenticated user
    is the invited user.

    **Permissions**
    - Authenticated user required.

    **Returns**
    - List of pending group invitations including group name.
    """

    return get_list_invitacion(session,status,current_user.id)


@router.get("/list_invitation/send",response_model=list[GroupInvitationRead],
               status_code=status.HTTP_200_OK)
async def list_invitation_send(    
    session: sessionDep,
    current_user: User = Depends(get_current_user),
    status:InvitationStatus=Query()
    ):
    """
    List pending,rejected,accepted invitations send for the current user.

    Retrieves all pending,rejected,accepted group invitations where the authenticated user
    is the invited user.

    **Permissions**
    - Authenticated user required.

    **Returns**
    - List of pending group invitations including group name.
    """

    return get_list_invitacion_send(session,status,current_user.id)
    

@router.post("/id_invitation/{id_invitation}/accept",status_code=status.HTTP_201_CREATED)
async def accept_invitation(session: sessionDep,
                            id_invitation:int,
                           current_user: User = Depends(get_current_user),
                           oso:Oso=Depends(get_oso)): 
    
    context=RequestContext(current_user, session)
    invitation=Invitation(invitation_id=id_invitation,invited_user_id=current_user.id)
    if not oso.is_allowed(context,"accept_invitation",invitation):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )    
    return accept_invitations(session,id_invitation)


@router.post("/id_invitation/{id_invitation}/reject",status_code=status.HTTP_201_CREATED)
def reject_invitation(session: sessionDep,
                            id_invitation:int,
                           current_user: User = Depends(get_current_user),
                           oso:Oso=Depends(get_oso)): 
    context=RequestContext(current_user, session)
    invitation=Invitation(invitation_id=id_invitation,invited_user_id=current_user.id)
    if not oso.is_allowed(context,"reject_invitation",invitation):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )    
    return reject_invitations(session,id_invitation)
    
    



      