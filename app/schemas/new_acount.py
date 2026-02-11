from typing import Optional
from pydantic import BaseModel, EmailStr, Field,SecretStr


class NewAcount(BaseModel):
    username:str
    full_name:str
    email:Optional[EmailStr] = None    
    disable:bool  | None = Field(default=False)
    password:SecretStr 

    
    

   
