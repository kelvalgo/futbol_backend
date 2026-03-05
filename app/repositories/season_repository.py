from sqlmodel import Session, select
from app.filter.season_filter import SeasonFilter
from app.models.season import Season


def list_season_repository(session:Session,id_group:int,param:SeasonFilter):

    statement = (
        select(Season)
        
        .where(
            Season.group_id == id_group,
            Season.is_active == param.disabled
        )
        .order_by(Season.group_id )
        .offset(param.skip)
        .limit(param.limit)
    )
    return session.exec(statement).all()