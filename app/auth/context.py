from sqlalchemy.orm import Session
from app.models.user import User

class RequestContext:
    def __init__(self, user:User, db:Session):
        self.user = user
        self.db = db