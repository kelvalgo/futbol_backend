


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

    # 🔹 Verificar si ya existen en GameTable
    stmt_game = select(GameTable.user_id).where(
        GameTable.user_id.in_(ids),
        GameTable.season_id == id_season
    )

    data_game = session.exec(stmt_game).all()

    # 🔹 Si NO hay datos en GameTable → traer de Skill
    if not data_game:

        stmt = (
            select(
                User.id,
                User.username,
                Skill.position,
                Skill.spatial_condition
            )
            .join(UserGroupF, UserGroupF.user_id == User.id)
            .join(Skill, Skill.user_group_id == UserGroupF.id)
            .where(
                User.id.in_(ids),
                UserGroupF.group_id == id_group
            )
        )

        data = session.exec(stmt).mappings().all()

        for d in data:
            gamer_data = Gamer(
            id_jugador=d["id"],
            jugador=d["username"],
            puntos=d.get("points", 0),
            estrellas=d.get("stars", 0),
            posicion=d["position"],
            mayor=d["spatial_condition"]
          )
           
            gamers_skill.append(gamer_data)

    # 🔹 Si SÍ hay datos → traer de GameTable + Skill
    else:

        stmt = (
            select(
                User.id,
                User.username,
                GameTable.points,
                GameTable.stars,
                Skill.position,
                Skill.spatial_condition
            )
            .join(UserGroupF, UserGroupF.user_id == User.id)
            .join(Skill, Skill.user_group_id == UserGroupF.id)
            .join(GameTable, GameTable.user_id == User.id)
            .where(
                User.id.in_(ids),
                UserGroupF.group_id == id_group,
                GameTable.season_id == id_season
            )
        )

        data = session.exec(stmt).mappings().all()

        for d in data:
            gamer_data = Gamer(
            id_jugador=d["id"],
            jugador=d["username"],
            puntos=d.get("points", 0),
            estrellas=d.get("stars", 0),
            posicion=d["position"],
            mayor=d["spatial_condition"]
          )
            gamers_skill.append(gamer_data)
         
    return gamers_skill