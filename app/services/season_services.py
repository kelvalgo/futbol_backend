from sqlmodel import Session
from app.filter.season_filter import SeasonFilter
from app.schemas.season import SeasonRead, SeasonUpdatePatch
from app.repositories.season_repository import list_season_repository


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