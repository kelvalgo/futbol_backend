from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import SecretStr
from app.auth.context import RequestContext
from app.models.group_friends import GroupFriends
from app.db.db import sessionDep
from app.core.security.security import get_current_user
from app.models.user import User
from app.schemas.group_friends import GroupFriendCreate, GroupFriendRead
from app.schemas.user import UserCreate, UserRead,NewAcount
from app.services.groupf_service import create_group_friend
from app.services.user_service import create_new_password,list_users_of_group,create_users_by_group,create_new_acount
from app.filter.group_filter import UserGroupFilter
from app.core.enums.auth_results import AuthResult


from oso import Oso
from app.auth.oso import get_oso



router=APIRouter(prefix="/group", tags=["Group"])



@router.post("/new_group",
             status_code=status.HTTP_201_CREATED)
async def new_group(session: sessionDep,
                    data:GroupFriendCreate,   
                    current_user: User = Depends(get_current_user)):
      
        """
        new group.

        **Permissions**
        - User logged.

        **Parameters**
        - **data**: Group.

        **Returns**
        - The newly group..
        """
        message=create_group_friend(session,data,current_user.id)
        
        return message
