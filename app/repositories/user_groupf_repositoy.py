from sqlmodel import Session
from app.models.user_groupf import UserGroupF



def create_user_groupf(session: Session,user_group:UserGroupF):         
        session.add(user_group)

