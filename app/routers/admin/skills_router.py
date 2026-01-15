from fastapi import APIRouter,Depends,HTTPException,status
from app.db.db import sessionDep
from sqlmodel import select
from app.core.security import  check_admin
from app.models.user import User
from app.models.skill import Skill
from app.schemas.skill import SkillRead,SkillCreate,SkillUpdatePut,SkillUpdatePatch


router=APIRouter(prefix="/skill", tags=["Admin - Skill"])


@router.get("/",response_model=list[SkillRead], 
            status_code=status.HTTP_200_OK)
async def list_skill(
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    return session.exec(select(Skill)).all()

@router.post("/",response_model=SkillRead,
             status_code=status.HTTP_201_CREATED)
def create_skill(skill_in:SkillCreate,
                 session: sessionDep,
                 current_user: User = Depends(check_admin)):
    
    template= select(Skill).where(skill_in.user_id==Skill.user_id)
    skill=session.exec(template).first()
    if skill:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Skills already exists"
        )
    skill_new = Skill(**skill_in.model_dump())
    session.add(skill_new)
    session.commit()
    session.refresh(skill_new)
    return skill_new
    
@router.delete("/{skill_id}",response_model=SkillRead,
               status_code=status.HTTP_200_OK)
async def delete_skill(
    skill_id:int,
    session:sessionDep,
    current:User=Depends(check_admin)
    ):
    skill=session.exec(select(Skill).where(Skill.id==skill_id)).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return skill


@router.put("/",
    response_model=SkillRead,
    status_code=status.HTTP_200_OK
)
def update_skill_put(
    Skill_in: SkillUpdatePut,
    session:sessionDep,
    current_user: User = Depends(check_admin)
    ):
    skill = session.get(Skill, Skill_in.id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    for field, value in Skill_in.model_dump().items():
        setattr(skill, field, value)

    session.commit()
    session.refresh(skill)
    return skill


@router.patch("/",
    response_model=SkillRead,
    status_code=status.HTTP_200_OK
)
def update_skill_patch(
    skill_in: SkillUpdatePatch,
    session: sessionDep,
    current_user: User = Depends(check_admin)
):
    skill = session.get(Skill, skill_in.id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    data = skill_in.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for field, value in data.items():
        setattr(skill, field, value)

    session.commit()
    session.refresh(skill)
    return skill
    