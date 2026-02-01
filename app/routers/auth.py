from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.schemas.token import Token
from app.core.security.token_jwt import create_access_token
from app.db.db import sessionDep
from app.core.security.token_jwt import decode_token
from app.models.user import User
from app.core.security.hashing import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_user(username:str,db: Session):
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()

def autenticate_user(username:str, password:str,db: Session):
    user = get_user(username,db)
    if not user or not verify_password(password, user.hashed_password) :
        return None
    return user


@router.post("/token",response_model=Token)
async def login(db: sessionDep,form_data: OAuth2PasswordRequestForm = Depends() ):
    user = autenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401, detail="invalidated credentials")
    access_token=create_access_token(data={"sub":user.username})
    return {
        "access_token":access_token,
        "token_type":"bearer"
        }