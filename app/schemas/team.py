from pydantic import BaseModel, Field
from typing import List, Optional
from app.core.enums.position_enum import PositionEnum



class Gamer(BaseModel):
    id_jugador:int 
    jugador: str
    puntos: int = Field(default=0)
    estrellas: float = Field(default=0)
    posicion: PositionEnum  
    mayor: bool= Field(default=False)

class GamersOfGame(BaseModel):
    id_jugador:int  = Field(alias="id_user")

class GamersRequest(BaseModel):
    gamers: list[GamersOfGame]    

class EquipoResponse(BaseModel):
    nombre: str
    media_estrellas: float
    jugadores: List[Gamer]



class TeamGeneratorResponse(BaseModel):
    equipo_rojo: EquipoResponse
    equipo_azul: EquipoResponse
    banca: Optional[list[Gamer]] = None
    