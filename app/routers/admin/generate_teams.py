from fastapi import APIRouter, HTTPException,Depends,status
from app.core.security import check_admin
from app.models.user import User
from typing import List
from app.schemas.team import Jugador, GenerarEquiposResponse
from app.core.teams.team_generator import generar_equipos

router = APIRouter(prefix="/generate_teams", tags=["Admin - Generate Teams"])


@router.post("/generar", response_model=GenerarEquiposResponse,status_code=status.HTTP_200_OK)
async def generate_teams(jugadores: List[Jugador],current_user: User = Depends(check_admin)):
    try:
        return generar_equipos(jugadores)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

