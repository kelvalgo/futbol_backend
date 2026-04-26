from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.db.db import sessionDep
from app.core.security.token_jwt import decode_token
from app.models.user import User
from app.core.enums.status_enum import Status
from fastapi import Request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_user(username:str,db: Session):
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()

def get_current_user( request: Request,  db: sessionDep,
    token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    username = payload.get("sub")
    

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user(username,db)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if  user.status==Status.inactive:   # status == inactive
        raise HTTPException(
        status_code=403,
        detail="User inactive"
        )
    request.state.user = user if user else None
    return user


def check_admin(user:User=Depends(get_current_user)):
    if not user.admin:
        raise  HTTPException(status_code=403, detail="insufficient permissions") 
    return user
    