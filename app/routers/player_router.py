from fastapi import APIRouter,HTTPException,status
from app.models.player import  Player,Player_create,Player_update
from app.db.db import sessionDep
from sqlmodel import select

router=APIRouter()


@router.get("/player",response_model=list[Player],tags=["player"])
async def list_user(session: sessionDep):
      return session.exec(select(Player)).all()

@router.get("/player/{name_player}",response_model=list[Player],tags=["player"])
async def user(name_player:str,session: sessionDep):
    try:
        query = select(Player).where(Player.name == name_player)
        results = session.exec(query).all()
        return results
    except Exception as e:
        # Para depuración
        return {"error": str(e)}
    