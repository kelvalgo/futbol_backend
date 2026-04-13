


from sqlmodel import Session, select
from sqlmodel import Session
from app.auth.context import RequestContextMacth
from app.filter.match_filter import MacthSeasonGroupFilter
from app.models.game_table import GameTable
from app.models.group_friends import GroupFriends
from app.models.season import Season
from app.models.skill import Skill
from app.models.user import User
from app.models.user_groupf import UserGroupF
from app.schemas.team import Gamer, GamersRequest


def team_generator_repository(match_context:RequestContextMacth):
    pass

def find_data_gamers(session:Session,id_group:int,id_season:int,gamers_request:GamersRequest):
    gamers_skill: list[Gamer] = []

    # 🔹 Obtener ids
    ids = [gamer.id_jugador for gamer in gamers_request.gamers]

    # 🔹 Query única (Skill obligatorio + GameTable opcional)
    stmt = (
        select(
            User.id,
            User.username,
            GameTable.points,
            GameTable.stars,
            Skill.position,
            Skill.spatial_condition
        )
        .join(
            UserGroupF,
            (UserGroupF.user_id == User.id) &
            (UserGroupF.group_id == id_group)  # 🔥 mover aquí
        )
        .join(
            Skill,
            Skill.user_group_id == UserGroupF.id
        )
        .join(
            GameTable,
            (GameTable.user_id == User.id) &
            (GameTable.season_id == id_season),
            isouter=True
        )
        .where(
            User.id.in_(ids)
        )
    )

    data = session.exec(stmt).mappings().all()

    # 🔹 Transformar resultados
    for d in data:
        gamer_data = Gamer(
            id_jugador=d["id"],
            jugador=d["username"],
            puntos=d.get("points") or 0,      # maneja None
            estrellas=d.get("stars") or 0,    # maneja None
            posicion=d["position"],
            mayor=d["spatial_condition"]
        )

        gamers_skill.append(gamer_data)

    return gamers_skill