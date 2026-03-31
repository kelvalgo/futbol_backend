from app.core.enums.auth_results import AuthResult
from app.filter.group_filter import Group
from app.filter.match_filter import MacthSeasonGroupFilter
from app.models.user import User
from app.schemas.team import GamersOfGame, GamersRequest, TeamGeneratorResponse
from app.services.teams_generator_service import  team_generator_service
from fastapi import APIRouter,Depends, HTTPException, Query,status
from app.core.security.security import get_current_user
from app.db.db import sessionDep
from app.filter.pagination import Pagination
from app.auth.context import RequestContext, RequestContextMacth
from oso import Oso
from app.auth.oso import get_oso



router=APIRouter(prefix="/team_generator", tags=["Team Generator"])


@router.post("/id_group/{group_id}/match/{match_id}/season/{season_id}/internal",
               response_model=TeamGeneratorResponse,
               status_code=status.HTTP_200_OK)
async def get_list_teams(    
    session: sessionDep,
    group_id:int,
    match_id:int,
    season_id: int, 
    gamers:GamersRequest,
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    
   
    group = Group(id_group=group_id)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"get_list_teams",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    
    match_find = MacthSeasonGroupFilter(id_season=season_id,id_match=match_id)

   
    return  team_generator_service(session,group_id,match_find,gamers)
