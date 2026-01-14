from fastapi import APIRouter,Depends,HTTPException,status
from app.models.skill import  Skill
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserRead
from app.core.hashing import hash_password


router=APIRouter(prefix="/view", tags=["User"])
# 🔓 Solo usuarios autenticados
@router.get("/",response_model=list[UserRead],
               status_code=status.HTTP_200_OK)
async def list_user(
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):
    return session.exec(select(User)).all()

