from sqlmodel import Session
from app.repositories.user_repository import get_users_by_group


def list_users_of_group(
    session: Session,
    group_id: int,
    current_user):   
    return get_users_by_group(session, group_id)