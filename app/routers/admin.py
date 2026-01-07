from fastapi import APIRouter,Depends,HTTPException,status
from app.models.skill import  Skill,Skill_create,Skill_update
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import get_current_user, check_admin
from app.models.user import User
from app.shemas.user import User_read

router=APIRouter()
# 🔓 Solo usuarios autenticados
@router.get("/", response_model=list[User],tags=["Admin"])
async def list_user(
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):
    return session.exec(select(User)).all()


# 🔐 Solo ADMIN
@router.get("/admin", response_model=list[User_read],tags=["Admin"])
async def list_players_admin(
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    return session.exec(select(User)).all()