from app.auth.context import RequestContext, RequestContextMacth
from app.auth.oso import get_oso
from app.filter.match_filter import MacthSeasonGroupFilter, MatchFilter
from oso import Oso
from app.core.enums.auth_results import AuthResult
from app.filter.group_filter import Group
from app.schemas.season_match import SeasonMatchRead
from app.services.match_service import create_match_service, list_match, update_match_finished_service, update_match_service
from fastapi import APIRouter,Depends,HTTPException,status
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security.security import check_admin, get_current_user
from app.models.user import User
from app.models.match import Match
from app.schemas.match import MatchRead,MatchCreate, MatchUpdateFinishPatch,MatchUpdatePatch


router=APIRouter(prefix="/match", tags=["Match"])


@router.get("/id_group/{id_group}/",response_model=list[SeasonMatchRead],  
            status_code=status.HTTP_200_OK)
async def list_match_table( session: sessionDep,
    id_group:int,
    param:MatchFilter= Depends(),
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"list_match",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )

    list_matchs=list_match(session,id_group,param)

    return list_matchs




@router.post("/id_group/{id_group}/internal",
             status_code=status.HTTP_201_CREATED)
def create_match(id_group:int,                                 
                  session: sessionDep,
                  match_in:MatchCreate,  
                 current_user: User = Depends(get_current_user),
                 oso:Oso=Depends(get_oso)):   



    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if  oso.is_allowed(context,"create_match",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )

    return  create_match_service(session,id_group,match_in)


@router.patch("/id_group/{group_id}/match/{match_id}/season/{season_id}/internal",
    status_code=status.HTTP_200_OK
)
def update_match(session: sessionDep,
                 group_id:int,
                 match_id:int,
                 season_id: int,
                 match_pacth:MatchUpdatePatch,
                 current_user: User = Depends(get_current_user),
                 oso:Oso=Depends(get_oso)):     
    
    group = Group(id_group=group_id)
    match_find = MacthSeasonGroupFilter(id_season=season_id,id_group=group_id,id_match=match_id)
    context=RequestContextMacth(current_user, session,match_find)
    if  oso.is_allowed(context,"update_match",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    return update_match_service(session,match_find,match_pacth)


@router.patch("/id_group/{group_id}/match/{match_id}/season/{season_id}/internal/finished",
    status_code=status.HTTP_200_OK
)
def update_match_finish(session: sessionDep,
                 group_id:int,
                 match_id:int,
                 season_id: int,
                 match_pacth:MatchUpdateFinishPatch,
                 current_user: User = Depends(get_current_user),
                 oso:Oso=Depends(get_oso)):     
    
    group = Group(id_group=group_id)
    match_find = MacthSeasonGroupFilter(id_season=season_id,id_group=group_id,id_match=match_id)
    context=RequestContextMacth(current_user, session,match_find)
    if  oso.is_allowed(context,"update_match",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    return update_match_finished_service(session,match_find,match_pacth,season_id)


   