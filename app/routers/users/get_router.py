from fastapi import APIRouter,Depends,HTTPException,status
from app.models.group_friends import GroupFriends
from app.models.skill import  Skill
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserRead
from app.services.user_service import list_users_of_group


from oso import Oso
from app.auth.oso import get_oso



router=APIRouter(prefix="/view", tags=["User"])



@router.get("/{id_group}/id_group",response_model=list[UserRead],
               status_code=status.HTTP_200_OK)
async def list_user(
    id_group:int,
    session: sessionDep,
    current_user: User = Depends(get_current_user),
    oso:Oso=Depends(get_oso)
):
    # Validation 
    if not oso.is_allowed(current_user.id, "user", id_group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Forbidden"
        )
    return list_users_of_group(session,id_group,current_user)


'''
# 🔓 Solo usuarios autenticados
@router.get("/",response_model=list[UserRead],
               status_code=status.HTTP_200_OK)
async def list_user(
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):
    return session.exec(select(User)).all()
'''

