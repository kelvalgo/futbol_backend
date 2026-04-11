from http.client import HTTPException

from sqlmodel import Session,select
from app.core.enums.match_status import MatchStatus
from app.core.enums.status_enum import Status
from app.filter.season_filter import SeasonFilter
from app.models.match import Match
from app.models.season import Season
from app.models.user import User
from app.models.match_player import MatchPlayer
from app.schemas.match_player import  MatchPlayerCreate, MatchPlayerUpdatePatch
from app.models.match_player import MatchPlayer
from fastapi import APIRouter,Depends,HTTPException,status

def list_match_player_repository(session:Session,group_id:int):
    
    statement = (
        select(MatchPlayer,User.username)
        .join(User, User.id == MatchPlayer.user_id,)
        .join(Match, Match.id==MatchPlayer.match_id)
        .join(Season,Season.id==Match.season_id)
        .where( Season.group_id==group_id,
               Match.status_match == MatchStatus.in_progress.value
        )
        .order_by(MatchPlayer.team,User.username)
    )


    print(f"select ***********{statement}")
    return session.exec(statement).all()      

def create_match_player_repository(session:Session, players:list[MatchPlayerCreate]):
    db_players = []
   
    for player in players:
        db_player = MatchPlayer(
            match_id=player.match_id,
            user_id=player.user_id,
            team=player.team,
            position=player.position,
            goals_scored=player.goals_scored,
            goals_conceded_as_goalkeeper=player.goals_conceded_as_goalkeeper
        )
        db_players.append(db_player)
    
    try:
        session.add_all(db_players)  # 🔥 inserta todo en bloque
        session.commit()
    except Exception as e:
        print("ERROR INSERTANDO MATCH PLAYERS:", e)
        session.rollback()
        raise
    return db_players

def find_match_player_repository(session:Session, id_match_player:int):
    match_player = session.get(MatchPlayer, id_match_player)
    return match_player


def update_match_player_repository(session:Session,match_player_id:int,match_player_pacth:MatchPlayerUpdatePatch):
    
    match_player = find_match_player_repository(session, match_player_id)
    if not match_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Match player not found"
        )

    update_data = match_player_pacth.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
            setattr(match_player, field, value)

    return match_player