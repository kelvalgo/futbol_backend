from sqlmodel import Session, select
from app.schemas.season import SeasonBase, SeasonCreate, SeasonUpdatePatch
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

def create_season_repositoy(session:Session,id_group:int,param:SeasonBase):

    new_season=Season(name=param.name,
                      year=param.year,
                      is_active=param.is_active,
                      group_id=id_group)

    session.add(new_season)

    return new_season

def find_season(session:Session,id_group:int,name:str,year:int):
    template= select(Season).where(name==Season.name,Season.year == year,Season.group_id==id_group)
    season=session.exec(template).first()
    return season


def update_season_repository(session:Session,group_id:int,id_season:int,param:SeasonUpdatePatch):
        db_season = session.exec(
            select(Season).where(
                Season.id == id_season,
                Season.group_id == group_id
            )
        ).first()

        if not db_season:
            raise ValueError(
                f"Season {id_season} not found for group {group_id}"
            )

        update_data = param.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_season, field, value)

        return db_season
         
