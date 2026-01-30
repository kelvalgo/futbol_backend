from dotenv import load_dotenv
import os

_ = load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int (os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),30)

if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY no configurada")



