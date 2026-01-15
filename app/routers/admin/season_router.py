from fastapi import APIRouter,Depends,HTTPException,status
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import check_admin
from app.models.user import User
from app.models.season import Season
from app.schemas.season import SeasonRead,SeasonCreate,SeasonUpdatePut,SeasonUpdatePatch


router=APIRouter(prefix="/season", tags=["Admin - Season"])


@router.get("/",response_model=list[SeasonRead], 
            status_code=status.HTTP_200_OK)
async def list_season_table(
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    return session.exec(select(Season)).all()


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
    current_user: User = Depends(check_admin)
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
    
    