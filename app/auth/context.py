from sqlalchemy.orm import Session
from app.filter.match_filter import MacthSeasonGroupFilter
from app.models.user import User

class RequestContext:
    def __init__(self, user:User, db:Session):
        self.user = user
        self.db = db

class RequestContextMacth:
    def __init__(self, user:User, db:Session, macth_find:MacthSeasonGroupFilter):
        self.user = user
        self.db = db
        self.macth_find=macth_find
