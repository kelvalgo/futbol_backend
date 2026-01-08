from fastapi import APIRouter,Depends,HTTPException,status
from app.models.skill import  Skill,Skill_create,Skill_update
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import get_current_user, check_admin
from app.models.user import User,User_create
from app.shemas.user import User_read
from app.core.hashing import hash_password


router=APIRouter(prefix="/admin", tags=["Admin"])
# 🔓 Solo usuarios autenticados
@router.get("/",response_model=list[User])
async def list_user(
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):
    return session.exec(select(User)).all()


# 🔐 Solo ADMIN
@router.get("/",response_model=list[User_read])
async def list_players_admin(
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    return session.exec(select(User)).all()

@router.post("/",response_model=User_read)
async def create_user(
    session: sessionDep,
    user_in:User_create,
    current_user: User = Depends(check_admin)
    ):
    user_new = User(**user_in.model_dump())
    user_new.hashed_password = hash_password("Inicio")

    session.add(user_new)
    session.commit()
    session.refresh(user_new)
    return user_new