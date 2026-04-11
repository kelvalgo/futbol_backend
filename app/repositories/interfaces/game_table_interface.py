from abc import ABC, abstractmethod

from sqlmodel import Session
from app.schemas.match_player import MatchPlayer, MatchPlayerStarts
from app.schemas.match import MatchUpdatePatch
from app.schemas.game_table import ListGameTable

class GameTableInterface(ABC):

    @abstractmethod
    def find_match_player_teams_repository(self,session:Session, id_match:int)-> list[MatchPlayer]:
        pass
    @abstractmethod
    def find_starts_for_player_repository(self,session:Session,match_players:list[MatchPlayer])-> list[MatchPlayerStarts]:
        pass
    @abstractmethod
    def goalkeeper_goals_conceded_repository(self,match_players:list[MatchPlayerStarts],match_pacth:MatchUpdatePatch)-> list[MatchPlayerStarts]:
        pass
    @abstractmethod
    def list_game_table_user_repository(self,match_players:list[MatchPlayerStarts],match_pacth:MatchUpdatePatch,season_id:int)-> list[ListGameTable]:
        pass    