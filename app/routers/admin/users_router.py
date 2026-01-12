from fastapi import APIRouter,Depends,HTTPException,status
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import get_current_user, check_admin
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate,UserCreate
from app.core.hashing import hash_password


router=APIRouter(prefix="/admin/user", tags=["Admin - User"])


@router.get("/",response_model=list[UserRead],
               status_code=status.HTTP_200_OK)
async def list_user(
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    return session.exec(select(User)).all()

@router.post("/",response_model=UserRead,
               status_code=status.HTTP_201_CREATED)
async def create_user(
    session: sessionDep,
    user_in:UserCreate,
    current_user: User = Depends(check_admin)
    ):

    template= select(User).where(user_in.username==User.username)
    user=session.exec(template).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    user_new = User(**user_in.model_dump())
    user_new.hashed_password = hash_password("Inicio")

    session.add(user_new)
    session.commit()
    session.refresh(user_new)
    return user_new

@router.delete("/{user_id}",response_model=UserRead,
               status_code=status.HTTP_200_OK)
async def delete_user(
    user_id:int,
    session:sessionDep,
    current:User=Depends(check_admin)
    ):
    user=session.exec(select(User).where(User.id==user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return user

@router.put("/",
    response_model=UserRead,
    status_code=status.HTTP_200_OK
)
def update_user_put(
    user_in: UserUpdate,
    session:sessionDep,
    current_user: User = Depends(check_admin)
    ):
    user = session.get(User, user_in.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_in.model_dump().items():
        setattr(user, field, value)

    session.commit()
    session.refresh(user)
    return user

@router.patch("/",
    response_model=UserRead,
    status_code=status.HTTP_200_OK
)
def update_user_patch(
    user_in: UserUpdate,
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    user = session.get(User, user_in.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    data = user_in.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for field, value in data.items():
        setattr(user, field, value)

    session.commit()
    session.refresh(user)
    return user


@router.put("/user_id/{id}/pass/{new_password}",
            response_model=UserRead,
            status_code=status.HTTP_200_OK)
async def user_new_password(
    id:int,
    new_pass:str,
    session: sessionDep,
    current_user: User = Depends(get_current_user)
):
  user= session.get(User,id)
  new_hash=hash_password(new_pass)
  user.hashed_password=new_hash
  session.commit()
  session.refresh(user)
  return user