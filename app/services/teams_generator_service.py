from sqlmodel import Session
from app.auth.context import RequestContextMacth
from app.core.enums.match_status import MatchStatus
from app.core.enums.team_enum import TeamEnum
from app.filter.match_filter import MacthSeasonGroupFilter
from app.repositories.match_player_repository import create_match_player_repository
from app.repositories.match_repository import create_match_repositoy, find_match, find_match_id, update_match_rating_repositoy
from app.repositories.team_generator_repository import find_data_gamers  
from app.schemas.match import MatchUpdatePatchRating
from app.schemas.match_player import MatchPlayerCreate
from app.schemas.team import GamersRequest
from app.services.team_generator import generar_equipos
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException,status



def team_generator_service(session:Session,id_group:int,match_find:MacthSeasonGroupFilter,gamers:GamersRequest):
  
    gamers_data_skill=find_data_gamers(session,id_group,match_find.id_season,gamers)     


    try:
        
       
        match_in_progress= find_match_id(session,match_find.id_match,id_group,MatchStatus.in_progress)

       
        if match_in_progress:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="match in progress"
            )    


        
        team_generator= generar_equipos(gamers_data_skill)


        
        match_rating=MatchUpdatePatchRating(team_rating_blue= team_generator.equipo_azul.media_estrellas,
                                            team_rating_red=team_generator.equipo_rojo.media_estrellas,
                                            status_match=MatchStatus.in_progress)

        

        update_match_rating_repositoy(session,match_find,match_rating) 


        
        players:list[MatchPlayerCreate]=[]

        def process(team_players, team_enum):
            for p in team_players:
                players.append(
                    MatchPlayerCreate(
                        match_id=match_find.id_match,
                        user_id=p.id_jugador,
                        team=team_enum,
                        position=p.posicion,
                        goals_scored=0,
                        goals_conceded_as_goalkeeper=0
                    )
                )

        process(team_generator.equipo_rojo.jugadores, TeamEnum.red)
        process(team_generator.equipo_azul.jugadores, TeamEnum.blue)

        if team_generator.banca:
            process(team_generator.banca, TeamEnum.bench)
        
        create_match_player_repository(session,players)
        session.commit()
        return team_generator
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

