from pydantic import BaseModel, SecretStr


class NewPassword(BaseModel):

    current_password: SecretStr
    new_password: SecretStr