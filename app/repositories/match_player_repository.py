from sqlmodel import Session,select
from app.core.enums.match_status import MatchStatus
from app.core.enums.status_enum import Status
from app.filter.season_filter import SeasonFilter
from app.models.match import Match
from app.models.season import Season
from app.models.user import User
from app.models.match_player import MatchPlayer
from app.schemas.match_player import  MatchPlayerCreate
from app.models.match_player import MatchPlayer


def list_match_player_repository(session:Session,group_id:int):
    '''
    def list_match_player_repository(session:Session,group_id:int,param:MacthSeasonGroupFilter):
    
        statement = (
            select(Match,Season.name)
            .join(Season, Season.id == Match.season_id,)
            .where(
                Season.group_id==group_id,
                Match.id == param.id_match,
                Match.season_id==param.id_season
            )
            .order_by(Match.match_date)
        )
        '''  
    
    

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