from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    JWT_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PERIODING_DONATION:int
    LIMIT_GROUPS:int

    class Config:
        env_file = ".env"

settings = Settings()



