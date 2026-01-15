from fastapi import APIRouter,Depends,HTTPException,status
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import check_admin
from app.models.user import User
from app.models.match import Match
from app.schemas.match import MatchRead,MatchCreate,MatchUpdatePut,MatchUpdatePatch


router=APIRouter(prefix="/match", tags=["Admin - Match"])


@router.get("/",response_model=list[MatchRead], 
            status_code=status.HTTP_200_OK)
async def list_match_table(
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    return session.exec(select(Match)).all()


@router.post("/",response_model=MatchRead,
             status_code=status.HTTP_201_CREATED)
def create_match(match_in:MatchCreate,
                 session: sessionDep,
                 current_user: User = Depends(check_admin)):
    template= select(Match).where(match_in.season_id==Match.season_id,Match.match_date == match_in.match_date)
    
    match=session.exec(template).first()
    if match:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Match already exists"
        )
     
    match_new = Match(**match_in.model_dump())
    session.add(match_new)
    session.commit()
    session.refresh(match_new)
    return match_new
   
@router.delete("/{match_id}",response_model=MatchRead,
               status_code=status.HTTP_200_OK)
async def delete_match(
    match_id:int,
    session:sessionDep,
    current:User=Depends(check_admin)
    ):
    current_match=session.exec(select(Match).where(Match.id==match_id)).first()
    if not current_match:
        raise HTTPException(status_code=404, detail="Match not found")
    session.delete(current_match)
    session.commit()
    return current_match 


@router.put("/",
    response_model=MatchRead,
    status_code=status.HTTP_200_OK
)
def update_match_put(
    match_in: MatchUpdatePut,
    session:sessionDep,
    current_user: User = Depends(check_admin)
    ):
    match = session.get(Match, match_in.id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    for field, value in match_in.model_dump().items():
        setattr(match, field, value)

    session.commit()
    session.refresh(match)
    return match


@router.patch("/",
    response_model=MatchRead,
    status_code=status.HTTP_200_OK
)
def update_match_patch(
    match_in: MatchUpdatePatch,
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    match = session.get(Match, match_in.id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    data = match_in.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for field, value in data.items():
            setattr(match, field, value)

    session.commit()
    session.refresh(match)
    return match
    
    