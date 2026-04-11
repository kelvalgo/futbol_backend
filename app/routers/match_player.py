from app.auth.context import RequestContext, RequestContextMacth
from app.auth.oso import get_oso
from app.filter.match_filter import  MacthSeasonGroupFilter, MatchFilter
from app.schemas.match_player import MatchPlayerRead, MatchPlayerUpdatePatch
from app.services.match_player_service import list_match_player_service, update_match_player_service
from oso import Oso
from app.core.enums.auth_results import AuthResult
from app.filter.group_filter import Group
from app.schemas.season_match import SeasonMatchRead
from app.services.match_service import create_match_service, list_match, update_match_service
from fastapi import APIRouter,Depends,HTTPException,status
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security.security import check_admin, get_current_user
from app.models.user import User
from app.models.match import Match
from app.schemas.match import MatchRead,MatchCreate,MatchUpdatePatch


router=APIRouter(prefix="/match_player", tags=["Match_Player"])


@router.get("/id_group/{id_group}",response_model=list[MatchPlayerRead],
            status_code=status.HTTP_200_OK)
async def list_match_player( session: sessionDep,
    id_group:int,
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"list_match_player",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    list_matchs_player=list_match_player_service(session,id_group)

    return list_matchs_player


@router.patch("/id_group/{group_id}/match_player/{match_player_id}/internal",
    status_code=status.HTTP_200_OK
)
def update_match_player(session: sessionDep,
                 id_group:int,
                 match_player_id:int,
                 match_player_pacth:MatchPlayerUpdatePatch,
                 current_user: User = Depends(get_current_user),
                 oso:Oso=Depends(get_oso)):     
    
    group = Group(id_group=id_group) 
    context=RequestContext(current_user, session)

    x = oso.is_allowed(context,"update_match_player",group)
    if not oso.is_allowed(context,"update_match_player",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    return update_match_player_service(session,match_player_id,match_player_pacth)

       