from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session
from app.core.enums.status_enum import Status
from app.filter.season_filter import SeasonFilter
from app.schemas.season import SeasonBase, SeasonCreate, SeasonRead, SeasonUpdatePatch
from app.repositories.season_repository import  create_season_repositoy, find_season, list_season_repository, update_season_repository
from sqlalchemy.exc import SQLAlchemyError


def list_season_services(session:Session,id_group:int,param:SeasonFilter)->list[SeasonUpdatePatch]:

    seasons= list_season_repository(session,id_group,param)

    if not seasons:
        return []

    result = []

    for season in seasons:
        result.append(
            SeasonRead(
                id=season.id,
                name=season.name,
                year=season.year,
                is_active=season.is_active
            )
        )

    return result


def create_season_service(session:Session,id_group:int,param:SeasonCreate):

    try:    
        year_now=datetime.now().year
        season=find_season(session,id_group,param.name,year_now)
        if season:
            raise HTTPException(
                status_code=Status.HTTP_409_CONFLICT,
                detail="Season already exists"
        )

        new_season=SeasonBase(name=param.name,year=year_now,
                              is_active=Status.active)

        create_season_repositoy(session,id_group,new_season)        
        session.commit()
        return  {"message": "Season create successfully"}  
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )



def update_season_service(session:Session,group_id:int,id_season:int,param:SeasonUpdatePatch):

    try:
        update_season_repository(session,group_id,id_season,param)
        session.commit()
        return  {"message": "Session update successfully"}  
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        ) 
    

   
    