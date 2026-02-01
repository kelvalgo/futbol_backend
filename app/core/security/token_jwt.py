from datetime import datetime, timedelta,timezone
from jose import jwt
from jose.exceptions import JWTError

SECRET_KEY = "CAMBIA_ESTO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError as e:
        raise Exception(f"invalited or expired token {e}")
    
if __name__ == "__main__":

    user_data={"sub":"usuario123"}
    token= create_access_token(user_data)   
    print(f"token generated: \n {token} \n")

    try:
       decoded= decode_token(token)
       print(f"token decoded: \n {decoded} \n")
    except Exception as e:
        raise Exception(str(e))   