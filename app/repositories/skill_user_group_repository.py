from sqlmodel import Session,select
from app.models.user import User
from app.models.group_friends import GroupFriends
from app.models.user_groupf import UserGroupF
from app.models.skill import Skill
from app.schemas.user_group_bulk_filter import UserGroupBulkFilter

def list_skill(session:Session,group_id:int,param:UserGroupBulkFilter):
    
    statement = (
        select(Skill, User.username, User.id)
        .join(UserGroupF, Skill.user_group_id == UserGroupF.id)
        .join(User, User.id == UserGroupF.user_id)
        .join(GroupFriends, GroupFriends.id == UserGroupF.group_id)
        .where(
            GroupFriends.id == group_id,
            UserGroupF.disable == param.user_disabled
        )
        .order_by(User.username)
        .offset(param.skip)
        .limit(param.limit)
    )
       
    return session.exec(statement).all()      

  