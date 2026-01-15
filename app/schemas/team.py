from pydantic import BaseModel
from typing import List, Optional
from app.core.enum.position_enum import PositionEnum


class Jugador(BaseModel):
    id_jugador:int
    jugador: str
    puntos: int = 0
    estrellas: float = 0
    posicion: PositionEnum
    mayor: bool = False


class EquipoResponse(BaseModel):
    nombre: str
    media_estrellas: float
    jugadores: List[Jugador]


class GenerarEquiposResponse(BaseModel):
    equipo_rojo: EquipoResponse
    equipo_azul: EquipoResponse
    banca: Optional[Jugador] = None