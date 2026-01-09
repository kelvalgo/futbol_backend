from pydantic import BaseModel,EmailStr,field_validator
from sqlmodel import SQLModel,Field,Relationship, Session,select
from typing import Optional, TYPE_CHECKING
#from app.db.db import engine

if TYPE_CHECKING:
    from app.models.skill import Skill
    from app.models.game import Game

class User_base(SQLModel):
    username:str = Field(index=True, unique=True)
    email:Optional[EmailStr] = None
    full_name:str
    admin:bool=Field(default=False)
    disable:bool

    '''
    @field_validator("email")
    @classmethod
    def validate_email(cls,value):
        session=Session(engine)
        query=select(User).where(User.email==value)
        result=session.exec(query).first()
        if result :
            raise ValueError("This email is already registerd")  

        return value
        '''


class User_create (User_base):      
    pass

class User_update (User_base):  
    pass 


class User(User_base,table=True):
    id:int|None=Field(default=None,primary_key=True)
    hashed_password:str
    skill: Optional["Skill"] = Relationship(back_populates="user",
                                            sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    games: Optional["Game"] = Relationship(back_populates="user",
                                           sa_relationship_kwargs={"cascade": "all, delete-orphan"})

   