from sqlmodel import Session, select
from app.db.db import engine
from app.models.user_groupf import UserGroupF


def is_member_of_group(user_id: int, groupf_id: int) -> bool:
    with Session(engine) as session:
        try:
            statement = select(UserGroupF).where(
                UserGroupF.user_id == user_id,
                UserGroupF.group_id == groupf_id
            )
           
            result = session.exec(statement).first()
            
            return result is not None 
        except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False