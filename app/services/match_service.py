from app.core.enums.match_status import MatchStatus
from app.filter.match_filter import MacthSeasonGroupFilter, MatchFilter
from app.filter.season_filter import SeasonFilter
from app.repositories.match_repository import create_match_repositoy, find_match, list_match_repository, update_match_repository
from app.repositories.season_repository import find_season, find_season_activate, list_season_repository
from app.schemas.match import MatchCreate, MatchCreateBD, MatchUpdatePatch
from app.schemas.season_match import SeasonMatchRead
from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session
from app.filter.user_group_filter import UserGroupFilter
from sqlalchemy.exc import SQLAlchemyError
from app.core.enums.status_enum import Status



def list_match(session:Session,group_id:int,param:MatchFilter): 
    
    matchs = list_match_repository(session, group_id, param)
   
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
    
    return result

def create_match_service(session:Session,id_group:int,match_in:MatchCreate): 
   
    try:  
        
        season=find_match(session,id_group,MatchStatus.scheduled)
        if season:            
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Match already exists"
        )
        
        param=SeasonFilter(disabled=Status.active)
        seasonfind= find_season_activate(session,id_group,match_in.season_id,param)
        if seasonfind:
            
            match_bd=MatchCreateBD(season_id=match_in.season_id,
                                match_date=match_in.match_date.strftime("%Y-%m-%d")    
            )
            
            create_match_repositoy(session,match_bd)     
           
            session.commit()
            
            return  {"message": "Match create successfully"}  
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

def update_match_service(session:Session,match_find:MacthSeasonGroupFilter,match_pacth:MatchUpdatePatch):
   
    try:
        update_match_repository(session,match_find,match_pacth)
        session.commit()
        return  {"message": "Match update successfully"}  
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        ) 
    
        