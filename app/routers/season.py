from fastapi import APIRouter,Depends,HTTPException,status
from app.filter.season_filter import SeasonFilter
from app.filter.group_filter import Group
from app.services.season_services import list_season_services
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security.security import check_admin, get_current_user
from app.models.user import User
from app.models.season import Season
from app.schemas.season import SeasonRead,SeasonCreate,SeasonUpdatePut,SeasonUpdatePatch
from app.auth.context import RequestContext
from oso import Oso
from app.auth.oso import get_oso
from app.core.enums.auth_results import AuthResult

router=APIRouter(prefix="/season", tags=["Season"])


@router.get("/id_group/{id_group}",response_model=list[SeasonRead], 
            status_code=status.HTTP_200_OK)
async def list_season(
    session: sessionDep,
    id_group:int,
    param:SeasonFilter= Depends(),
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    

    group = Group(id_group=id_group)
    context=RequestContext(current_user, session)
    if not oso.is_allowed(context,"list_season",group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=AuthResult.FORBIDDEN.value
        )
    


    return   list_season_services(session,id_group,param)


@router.post("/",response_model=SeasonRead,
             status_code=status.HTTP_201_CREATED)
def create_season(season_in:SeasonCreate,
                 session: sessionDep,
                 current_user: User = Depends(check_admin)):
    template= select(Season).where(season_in.name==Season.name,Season.year == season_in.year)
    
    season=session.exec(template).first()
    if season:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Season already exists"
        )
     
    season_new = Season(**season_in.model_dump())
    session.add(season_new)
    session.commit()
    session.refresh(season_new)
    return season_new
   
@router.delete("/{season_id}",response_model=SeasonRead,
               status_code=status.HTTP_200_OK)
async def delete_season(
    season_id:int,
    session:sessionDep,
    current:User=Depends(check_admin)
    ):
    current_season=session.exec(select(Season).where(Season.id==season_id)).first()
    if not current_season:
        raise HTTPException(status_code=404, detail="Season not found")
    session.delete(current_season)
    session.commit()
    return current_season 


@router.put("/",
    response_model=SeasonRead,
    status_code=status.HTTP_200_OK
)
def update_season_put(
    season_in: SeasonUpdatePut,
    session:sessionDep,
    current_user: User = Depends(check_admin)
    ):
    season = session.get(Season, season_in.id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    for field, value in season_in.model_dump().items():
        setattr(season, field, value)

    session.commit()
    session.refresh(season)
    return season


@router.patch("/",
    response_model=SeasonRead,
    status_code=status.HTTP_200_OK
)
def update_season_patch(
    season_in: SeasonUpdatePatch,
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):
    season = session.get(Season, season_in.id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    data = season_in.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for field, value in data.items():
            setattr(season, field, value)

    session.commit()
    session.refresh(season)
    return season
    
    