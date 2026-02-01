from fastapi import APIRouter,Depends,HTTPException,status
from app.models.skill import  Skill
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security.security import get_current_user
from app.models.user import User
from app.schemas.user import UserRead
from app.core.security.hashing import hash_password


router=APIRouter(prefix="/new_pass", tags=["User"])
# 🔓 Solo usuarios autenticados
@router.put("/{new_password}",
            response_model=UserRead,
            status_code=status.HTTP_200_OK)
async def new_password(
    new_pass:str,
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):
  user= session.get(User,current_user.id)
  new_hash=hash_password(new_pass)
  user.hashed_password=new_hash
  session.commit()
  session.refresh(user)
  return user
