from sqlmodel import Session,select
from app.core.enums.match_status import MatchStatus
from app.core.enums.status_enum import Status
from app.filter.season_filter import SeasonFilter
from app.models.season import Season
from app.models.match import Match
from app.filter.match_filter import MacthSeasonGroupFilter, MatchFilter
from app.schemas.match import MatchCreate, MatchCreateBD, MatchUpdatePatch,MatchUpdatePatchRating

def list_match_repository(session:Session,group_id:int,param:MatchFilter):

    statement = (
        select(Match,Season.name)
        .join(Season, Season.id == Match.season_id,)
        .where(
            Season.group_id==group_id,
            Match.status_match == param.status_match
        )
        .order_by(Match.match_date)
        .offset(param.skip)
        .limit(param.limit)
    )
       
    return session.exec(statement).all()      


def find_match(session:Session,group_id:int,statusmatch:MatchStatus):
    
    statement = (select(Match.id)
            .join(Season,Season.id==Match.season_id)
            .where(
                Season.group_id == group_id,
                Match.status_match == statusmatch
            )
            )
    match=session.exec(statement).first()
    
    return match

def find_match_id(session:Session,match_id:int,group_id:int,statusmatch:MatchStatus):
    statement = (select(Match.id)
            .join(Season,Season.id==Match.season_id)
            .where(
                Season.group_id == group_id,
                Match.status_match == statusmatch,
                Match.id==match_id
            )
            )
    match=session.exec(statement).first()
    return match  is not None 


def create_match_repositoy(session:Session,param:MatchCreateBD) :
       
        new_match=Match(season_id=param.season_id,
                      match_date=param.match_date
                      )

        session.add(new_match)
       
        return new_match

def update_match_repository(session:Session,match_find:MacthSeasonGroupFilter,match_pacth:MatchUpdatePatch):
        db_match = session.exec(
            select(Match).where(
                Match.id == match_find.id_match,
                Match.season_id == match_find.id_season
            )
        ).first()

        if not db_match:
            raise ValueError(
                f"Match {match_find.id_match} not found for season {match_find.id_season}"
            )

        update_data = match_pacth.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_match, field, value)

        return db_match


def update_match_rating_repositoy(session:Session,match_find:MacthSeasonGroupFilter,match_pacth:MatchUpdatePatchRating):
        db_match = session.exec(
            select(Match).where(
                Match.id == match_find.id_match,
                Match.season_id == match_find.id_season
            )
        ).first()

        if not db_match:
            raise ValueError(
                f"Match {match_find.id_match} not found for season {match_find.id_season}"
            )

        update_data = match_pacth.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_match, field, value)

        return db_match