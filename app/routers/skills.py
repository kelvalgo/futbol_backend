from fastapi import APIRouter,Depends,HTTPException,status
from app.services.skill_service import list_user_skill,create_skill_service, update_skill_service
from app.filter.group_filter import Group
from app.core.enums.auth_results import AuthResult
from app.filter.user_group_filter import UserGroupFilter
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security.security import get_current_user
from app.models.user import User
from app.models.skill import Skill
from app.schemas.skill import SkillRead,SkillCreate,SkillUpdatePatch
from app.auth.context import RequestContext
from oso import Oso
from app.auth.oso import get_oso




router=APIRouter(prefix="/skill", tags=["Skill"])


@router.get("/id_group/{id_group}/",response_model=list[SkillRead], 
            status_code=status.HTTP_200_OK)
async def list_skill(
    session: sessionDep,
    id_group:int,
    param:UserGroupFilter= Depends(),
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    """
    Retrieve a paginated list of skills for all users belonging to the specified group.

    - **id_group**: Identifier of the group.
    - **user_disabled** (query, optional): Filter users by disabled status.
    - **skip** (query, optional): Number of records to skip (pagination).
    - **limit** (query, optional): Maximum number of records to return (pagination).

    Authentication is required. Authorization policies are enforced to ensure
    the current user has permission to list skills within the specified group.
    """
    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"list_skill",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )

    users_skill=list_user_skill(session,id_group,param)

    return users_skill

@router.post("/id_group/{id_group}/internal",
             status_code=status.HTTP_201_CREATED)
def create_skill(session: sessionDep,
                 id_group:int,
                 users_skills:list[SkillCreate],
                 current_user: User = Depends(get_current_user),
                 oso:Oso=Depends(get_oso)):
    
    """
    Create one or multiple skills associated with a specific group.

    This endpoint allows an authenticated user to create skills for a given group.
    The user must have the required authorization to perform the "create_skill" action
    on the specified group.

    Path Parameters:
    - id_group (int): Unique identifier of the group where the skills will be created.

    Request Body:
    - users_skills (List[SkillCreate]): A list of skill objects to be created.

    Authorization:
    - Requires authenticated user.
    - Authorization is validated using Oso policies.

    Responses:
    - 201 Created: Skills successfully created.
    - 403 Forbidden: User does not have permission to create skills in this group.
    """
    
    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"create_skill",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
   
    return  create_skill_service(session,id_group,users_skills)
    

@router.patch("/id_group/{id_group}/internal",
    status_code=status.HTTP_200_OK
)
def update_skill(session: sessionDep,
                 id_group:int,
                 users_skills:list[SkillUpdatePatch],
                 current_user: User = Depends(get_current_user),
                 oso:Oso=Depends(get_oso)): 
    
    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"update_skill",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    return update_skill_service(session,id_group,users_skills)
    
    
    