from sqlmodel import Session, select
from app.core.enums.rol import Rol
from app.db.db import engine
from app.models.group_friends import GroupFriends
from app.models.user import User
from app.models.user_groupf import UserGroupF
from app.core.enums.status_enum import Status


def is_member_of_group(user: User, groupf: GroupFriends) -> bool:
    with Session(engine) as session:
        try:
            statement = select(UserGroupF).where(
                UserGroupF.user_id == user.id,
                UserGroupF.group_id == groupf.id,
            )
           
            result = session.exec(statement).first()
            
            return result is not None 
        except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False
        
def is_admin_of_group(user: User, groupf: GroupFriends) -> bool:
    with Session(engine) as session:
        try:
            statement = select(UserGroupF).where(
                UserGroupF.user_id ==  user.id,
                UserGroupF.group_id == groupf.id,
                UserGroupF.rol==Rol.admin
            )
           
            result = session.exec(statement).first()
            print(result)
            return result is not None 
        except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False       

def is_user_active(user:User) -> bool:  
    with Session(engine) as session:
        try:
            statement=select(User.status).where(
            User.id==user.id
            )
            status=session.exec(statement).first()
            return status==Status.active
        except Exception as e:
            print(f"Error in validation Oso: {e}")
            return False