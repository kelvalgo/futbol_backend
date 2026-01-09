from fastapi import APIRouter,Depends,HTTPException,status
from app.models.skill import  Skill,Skill_create,Skill_update
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import get_current_user, check_admin
from app.models.user import User, User_base,User_create
from app.shemas.user import User_read, User_update
from app.core.hashing import hash_password


router=APIRouter(prefix="/user", tags=["User"])
# 🔓 Solo usuarios autenticados
@router.get("/",response_model=list[User_read])
async def list_user(
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):
    return session.exec(select(User)).all()


@router.put("/{new_password}",
            response_model=User_read,
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
