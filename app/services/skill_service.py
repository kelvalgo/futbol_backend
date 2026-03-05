from sqlmodel import Session
from app.repositories.skill_repository import create_skills, update_skills
from app.schemas.skill import SkillCreate, SkillRead, SkillUpdatePatch
from app.repositories.skill_user_group_repository import list_skill
from app.filter.user_group_filter import UserGroupFilter
from sqlalchemy.exc import SQLAlchemyError


def list_user_skill (session:Session,group_id:int,param:UserGroupFilter)->SkillRead:
        
    skills = list_skill(session, group_id, param)

    if not skills:
        return []

    result = []

    for skill, username,id in skills:
        result.append(
            SkillRead(
                id=skill.id,
                user_id=id,
                user_name=username,
                position=skill.position,
                spatial_condition=skill.spatial_condition,
                gk=skill.gk,
                df=skill.df,
                mf=skill.mf,
                wf=skill.wf
            )
        )

    return result


def create_skill_service(session:Session,group_id:int,param:list[SkillCreate]):
    try:
        create_skills(session,group_id,param)
        session.commit()
        return  {"message": "Skills create successfully"}  
    except SQLAlchemyError:
        session.rollback()
        return False
    
def update_skill_service(session:Session,group_id:int,param:list[SkillUpdatePatch]):
    try:
        update_skills(session,group_id,param)
        session.commit()
        return  {"message": "Skills update successfully"}  
    except SQLAlchemyError:
        session.rollback()
        return False    
