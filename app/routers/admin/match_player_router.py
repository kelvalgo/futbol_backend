from fastapi import APIRouter,Depends,HTTPException,status
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import check_admin
from app.models.user import User
from app.models.match_player import MatchPlayer
from app.schemas.match_player import MatchPlayerRead,MatchPlayerCreate,MatchPlayerUpdatePut,MatchPlayerUpdatePatch


router=APIRouter(prefix="/match_player", tags=["Admin - MatchPlayer"])


@router.get("/",response_model=list[MatchPlayerRead], 
            status_code=status.HTTP_200_OK)
async def list_match_player_table(
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    return session.exec(select(MatchPlayer)).all()


@router.post("/",response_model=MatchPlayerRead,
             status_code=status.HTTP_201_CREATED)
def create_match_player(match_player_in:MatchPlayerCreate,
                 session: sessionDep,
                 current_user: User = Depends(check_admin)):
    template= select(MatchPlayer).where(match_player_in.match_id==MatchPlayer.match_id,MatchPlayer.user_id == match_player_in.user_id)
    
    match_player=session.exec(template).first()
    if match_player:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="MatchPlayer already exists"
        )
     
    match_player_new = MatchPlayer(**match_player_in.model_dump())
    session.add(match_player_new)
    session.commit()
    session.refresh(match_player_new)
    return match_player_new
   
@router.delete("/{match_player_id}",response_model=MatchPlayerRead,
               status_code=status.HTTP_200_OK)
async def delete_player_match(
    match_player_id:int,
    session:sessionDep,
    current:User=Depends(check_admin)
    ):
    current_match_player=session.exec(select(MatchPlayer).where(MatchPlayer.id==match_player_id)).first()
    if not current_match_player:
        raise HTTPException(status_code=404, detail="MatchPlayer not found")
    session.delete(current_match_player)
    session.commit()
    return current_match_player 


@router.put("/",
    response_model=MatchPlayerRead,
    status_code=status.HTTP_200_OK
)
def update_match_player_put(
    match_player_in: MatchPlayerUpdatePut,
    session:sessionDep,
    current_user: User = Depends(check_admin)
    ):
    match_player = session.get(MatchPlayer, match_player_in.id)
    if not match_player:
        raise HTTPException(status_code=404, detail="MatchPlayer not found")

    for field, value in match_player_in.model_dump().items():
        setattr(match_player, field, value)

    session.commit()
    session.refresh(match_player)
    return match_player


@router.patch("/",
    response_model=MatchPlayerRead,
    status_code=status.HTTP_200_OK
)
def update_match_player_patch(
    match_player_in: MatchPlayerUpdatePatch,
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    match_player = session.get(MatchPlayer, match_player_in.id)
    if not match_player:
        raise HTTPException(status_code=404, detail="MatchPlayer not found")

    data = match_player_in.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for field, value in data.items():
            setattr(match_player, field, value)

    session.commit()
    session.refresh(match_player)
    return match_player
    
    