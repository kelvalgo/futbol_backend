from app.core.enums.match_status import MatchStatus
from app.filter.match_filter import  MacthSeasonGroupFilter, MatchFilter
from app.filter.season_filter import SeasonFilter
from app.repositories.match_player_repository import list_match_player_repository
from app.repositories.match_repository import create_match_repositoy, find_match, list_match_repository, update_match_repository
from app.repositories.season_repository import find_season, find_season_activate, list_season_repository
from app.schemas.match import MatchCreate, MatchCreateBD, MatchUpdatePatch
from app.schemas.match_player import MatchPlayerRead
from app.schemas.season_match import SeasonMatchRead
from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session
from app.filter.user_group_filter import UserGroupFilter
from sqlalchemy.exc import SQLAlchemyError
from app.core.enums.status_enum import Status



def list_match_player_service(session:Session,group_id:int): 
    
    matchs_player = list_match_player_repository(session, group_id)
    
    response :list[MatchPlayerRead] = []

    for match_player, username in matchs_player:
        response.append({
            "id": match_player.id,
            "match_id": match_player.match_id,
            "user_id": match_player.user_id,
            "username": username,
            "team": match_player.team,
            "position": match_player.position,
            "goals_scored": match_player.goals_scored,
            "goals_conceded_as_goalkeeper": match_player.goals_conceded_as_goalkeeper
        })

    print(f"matchs_player***********{response}")
    '''
    if not matchs:
        return []

    result = []

    for match,season_name in matchs:
        result.append(
            SeasonMatchRead(
                id_match=match.id,
                id_season=match.season_id,
                name_season=season_name,
                match_date=match.match_date,
                blue_score=match.blue_score,                
                team_rating_blue=match.team_rating_blue,
                red_score= match.red_score,
                team_rating_red=match.team_rating_red,                
                win=match.win,
                status_match=match.status_match
            )
        )
    '''
    return response
