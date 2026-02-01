from fastapi import APIRouter,Depends,HTTPException,status
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security.security import check_admin
from app.models.user import User
from app.models.game_table import GameTable
from app.schemas.game_table import GameTableRead,GameTableCreate,GameTableUpdatePut,GameTableUpdatePatch


router=APIRouter(prefix="/game_table", tags=["Admin - GameTable"])


@router.get("/",response_model=list[GameTableRead], 
            status_code=status.HTTP_200_OK)
async def list_game_table(
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    return session.exec(select(GameTable)).all()


@router.post("/",response_model=GameTableRead,
             status_code=status.HTTP_201_CREATED)
def create_game_table(game_table_in:GameTableCreate,
                 session: sessionDep,
                 current_user: User = Depends(check_admin)):
    
    template= select(GameTable).where(game_table_in.user_id==GameTable.user_id)
    game_table=session.exec(template).first()
    if game_table:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Game table already exists"
        )
    game_table_new = GameTable(**game_table_in.model_dump())
    session.add(game_table_new)
    session.commit()
    session.refresh(game_table_new)
    return game_table_new
   
@router.delete("/{geme_table_id}",response_model=GameTableRead,
               status_code=status.HTTP_200_OK)
async def delete_game_table(
    game_table_id:int,
    session:sessionDep,
    current:User=Depends(check_admin)
    ):
    current_game_table=session.exec(select(GameTable).where(GameTable.id==game_table_id)).first()
    if not current_game_table:
        raise HTTPException(status_code=404, detail="Game table not found")
    session.delete(current_game_table)
    session.commit()
    return current_game_table


@router.put("/",
    response_model=GameTableRead,
    status_code=status.HTTP_200_OK
)
def update_game_table_put(
    game_table_in: GameTableUpdatePut,
    session:sessionDep,
    current_user: User = Depends(check_admin)
    ):
    game_table = session.get(GameTable, game_table_in.id)
    if not game_table:
        raise HTTPException(status_code=404, detail="Game table not found")

    for field, value in game_table_in.model_dump().items():
        setattr(game_table, field, value)

    session.commit()
    session.refresh(game_table)
    return game_table


@router.patch("/",
    response_model=GameTableRead,
    status_code=status.HTTP_200_OK
)
def update_game_table_patch(
    game_table_in: GameTableUpdatePatch,
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    game_table = session.get(GameTable, game_table_in.id)
    if not game_table:
        raise HTTPException(status_code=404, detail="Game table not found")

    data = game_table_in.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for field, value in data.items():
            setattr(game_table, field, value)

    session.commit()
    session.refresh(game_table)
    return game_table
    
    