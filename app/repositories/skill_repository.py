from sqlmodel import Session,select
from app.models.user_groupf import UserGroupF
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdatePatch


def create_skills(session:Session,group_id:int,param:list[SkillCreate])->list[Skill]:
    db_skills = []

    for skill_data in param:

        user_group = session.exec(
            select(UserGroupF).where(
                UserGroupF.user_id == skill_data.user_id,
                UserGroupF.group_id == group_id
            )
        ).first()

        if not user_group:
            raise ValueError(f"User {skill_data.user_id} is not in group {group_id}")

        db_skill = Skill(
            user_group_id=user_group.id,
            position=skill_data.position,
            spatial_condition=skill_data.spatial_condition,
            gk=skill_data.gk,
            df=skill_data.df,
            mf=skill_data.mf,
            wf=skill_data.wf
        )

        db_skills.append(db_skill)

    session.add_all(db_skills)
    return db_skills
    

def update_skills(session:Session,group_id:int,param:list[SkillUpdatePatch])->list[Skill]:
    updated_skills = []

    for skill_data in param:

        db_skill = session.exec(
            select(Skill)
            .join(UserGroupF)
            .where(
                UserGroupF.user_id == skill_data.user_id,
                UserGroupF.group_id == group_id
            )
        ).first()

        if not db_skill:
            raise ValueError(f"Skill for user {skill_data.user_id} not found")

        update_data = skill_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field != "user_id":
                setattr(db_skill, field, value)

        updated_skills.append(db_skill)

    return updated_skills