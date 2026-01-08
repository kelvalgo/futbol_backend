from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.shemas.token import Token
from app.core.token_jwt import create_access_token
from app.db.db import sessionDep
from app.core.token_jwt import decode_token
from app.models.user import User
from app.core.hashing import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")



def get_user(username:str,db: Session):
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()

def autenticate_user(username:str, password:str,db: Session):
    user = get_user(username,db)
    if not user or not verify_password(password, user.hashed_password) :
        return None
    return user

#dependences
'''
def get_current_user(   db: sessionDep,
    token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    username = payload.get("sub")

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user(username,db)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def check_admin(user:User=Depends(get_current_user)):
    if not user.admin:
        raise  HTTPException(status_code=403, detail="insufficient permissions") 
    return user
'''


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
'''
@router.get("/admin/")
async def admin_router(current_user: User=Depends(check_admin)):
    return{"msg":f"HI {current_user.full_name}, welcome panel admin"}  
'''