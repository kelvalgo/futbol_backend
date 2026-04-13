from pydantic import BaseModel

from app.core.enums.match_status import MatchStatus, MatchStatusRead
from app.filter.pagination import Pagination



class MatchFilter(Pagination):
    status_match:  MatchStatus


class MacthSeasonGroupFilter(BaseModel):
    id_season:int 
    id_match:int   

class MatchFilterRead(Pagination):
    status_match:  MatchStatusRead
    




    