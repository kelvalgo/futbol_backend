from app.core.enums.position_enum import PositionEnum
from app.core.enums.team_enum import TeamEnum
from app.core.enums.team_win_tie_lie_enum import TeamWinTieLieEnum
from app.models.match_player import MatchPlayer
from app.models.skill import Skill
from app.repositories.interfaces.game_table_interface import GameTableInterface
from sqlmodel import Session,select

from app.schemas.match import MatchUpdatePatch
from app.schemas.match_player import MatchPlayerStarts

class ListGameTable(GameTableInterface):

    def find_match_player_teams_repository(self,session:Session, id_match:int):
        match_players = session.exec(select(MatchPlayer).where(MatchPlayer.match_id == id_match).order_by(MatchPlayer.team)).all()
        return match_players

    def find_starts_for_player_repository(self,session:Session,match_players:list[MatchPlayer]):

        mactch_player_start:list[MatchPlayerStarts] = []

        statement = None



        for match_player in match_players:

        
            match match_player.position.value:
                case PositionEnum.GK.value:
                    statement = select(Skill.gk).where(Skill.user_group_id == match_player.user_id)
                case PositionEnum.DF.value:
                    statement = select(Skill.df).where(Skill.user_group_id == match_player.user_id)
                case PositionEnum.MF.value:
                    statement = select(Skill.mf).where(Skill.user_group_id == match_player.user_id)                        
                case PositionEnum.FW.value:
                    statement = select(Skill.wf).where(Skill.user_group_id == match_player.user_id) 

            skill_attr=session.exec(statement).first()
            
            
            player=MatchPlayerStarts(
                id=match_player.id,    
                match_id=match_player.match_id,
                user_id=match_player.user_id,           
                team=match_player.team,
                position=match_player.position,
                goals_scored=match_player.goals_scored,
                goals_conceded_as_goalkeeper=match_player.goals_conceded_as_goalkeeper,
                stars=skill_attr
            )
            mactch_player_start.append(player)

     
        return mactch_player_start

    def goalkeeper_goals_conceded_repository(self,match_players:list[MatchPlayerStarts],match_pacth:MatchUpdatePatch):   
        
        for p in match_players:
            if p.position.value == PositionEnum.GK.value and p.team.value == TeamEnum.blue.value:
                p.goals_conceded_as_goalkeeper = match_pacth.red_score
            elif p.position.value == PositionEnum.GK.value and p.team.value == TeamEnum.red.value:
                p.goals_conceded_as_goalkeeper = match_pacth.blue_score
        return match_players
    
    def list_game_table_user_repository(self,match_players:list[MatchPlayerStarts],match_pacth:MatchUpdatePatch,season_id:int):
        updated_players = [
                {
                    "user_id": p.user_id,
                    "season_id": season_id,
                    "team": p.team,
                    "games": 1,
                    "win": 1 if p.team == match_pacth.win else 0,
                    "lose": 1 if p.team != match_pacth.win and match_pacth.win != TeamWinTieLieEnum.tie else 0,
                    "tie": 1 if match_pacth.win == TeamWinTieLieEnum.tie else 0,
                    "player_goals_scored": p.goals_scored,
                    "goalkeeper_goals_conceded": p.goals_conceded_as_goalkeeper,
                    "stars": p.stars,
                    "points": (
                        1 if match_pacth.win == TeamWinTieLieEnum.tie
                        else 3 if p.team == match_pacth.win
                        else 0
                        ),
                    "fines": 0
                }
                for p in match_players
            ]
        return updated_players