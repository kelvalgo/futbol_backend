from sqlmodel import Session
from app.core.enums.position_enum import PositionEnum
from app.core.enums.team_enum import TeamEnum
from app.models import game_table
from app.models.season import Season
from app.filter.match_filter import MacthSeasonGroupFilter
from app.models.game_table import GameTable
from app.repositories.list_game_table import ListGameTable
from app.schemas.game_table import GameTableUpdatePatch   
from app.schemas.match import MatchUpdatePatch
from sqlmodel import Session,select

from app.schemas.match_player import MatchPlayer

def update_game_table_repository(session:Session,season_id:int,match_pacth:MatchUpdatePatch,match_players:list[MatchPlayer]):
    
        db_game_table = session.exec(
            select(GameTable.id).join(Season,Season.id == GameTable.season_id).where(
                GameTable.season_id == season_id
            )
        ).first()

        update_data = match_pacth.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_game_table, field, value)

        return db_game_table

def update_finish_game_table_repository(session:Session,season_id:int,match_pacth:MatchUpdatePatch,list_players:list[ListGameTable]):
        
        db_game_table = session.exec(
            select(GameTable).join(Season,Season.id == GameTable.season_id).where(
                GameTable.season_id == season_id
            )
        ).all()
        

        ####ojo solo es este if el que estas tocando lo demas queda igual
        if  db_game_table is None:
            
                     
            game_table=change_listGameTable_to_gameTable(list_players,season_id)

            session.add_all(game_table)   
        else:
               
                game_table_players=change_listGameTable_to_gameTable(list_players,season_id)

                    # 🔥 MAPEAR BD POR user_id
                db_map = {g.user_id: g for g in db_game_table}

                # 🔥 CAMPOS A SUMAR
                fields = [
                    "games",
                    "win",
                    "lose",
                    "tie",
                    "player_goals_scored",
                    "goalkeeper_goals_conceded",
                    "points"
                ]

                for player in game_table_players:
                    db_row = db_map.get(player.user_id)

                    if db_row:
                        # 🔥 SUMAR CAMPOS
                        for field in fields:
                            setattr(
                                db_row,
                                field,
                                getattr(db_row, field) + getattr(player, field, 0)
                            )
                    else:
                        # 🔥 SI NO EXISTE → INSERTAR
                        session.add(player)

                session.commit()  
                  
    
                       

'''
        update_data = match_pacth.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_game_table, field, value)
           

        return db_game_table '''
pass

def change_listGameTable_to_gameTable(list_players:list[ListGameTable],season_id:int)-> list[GameTable]:
    print("change_listGameTable_to_gameTable*************************************************")
    game_table:list[GameTable] = []
            
    for list_player in list_players:
        new_row = GameTable(
            user_id=list_player["user_id"],
            season_id=season_id,
            games=list_player.get("games", 0),
            win=list_player.get("win", 0),
            lose=list_player.get("lose", 0),
            tie=list_player.get("tie", 0),
            player_goals_scored=list_player.get("player_goals_scored", 0),
            goalkeeper_goals_conceded=list_player.get("goalkeeper_goals_conceded", 0),
            stars=list_player.get("stars", 0),
            points=list_player.get("points", 0),
            fines=list_player.get("fines", 0)
        )

        game_table.append(new_row)           

    return game_table