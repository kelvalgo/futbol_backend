from sqlmodel import Session
from app.models.user_groupf import UserGroupF
from sqlmodel import Session,select
from app.models.group_friends import GroupFriends
from app.models.user import User
from app.models.user_groupf import UserGroupF


def create_user_groupf(session: Session,user_group:UserGroupF):         
        session.add(user_group)

def update_usergroupf(session,data: tuple,param):
        group_id, user_id = data
        db_userg = session.exec(
        select(UserGroupF)
        .where(
                UserGroupF.user_id == user_id,
                UserGroupF.group_id == group_id
        )
        ).first()
        if not db_userg:
                raise ValueError(f"data for user {user_id} not found")

        update_data = param.model_dump(exclude_unset=True)

        for field, value in update_data.items():
                if field != "user_id":
                        setattr(db_userg, field, value)
        
        session.add(db_userg)

        return db_userg
         
   

