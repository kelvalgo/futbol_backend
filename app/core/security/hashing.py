#from passlib.context import CryptContext
import bcrypt

def hash_password(password: str) -> str:
    salt=bcrypt.gensalt()
    hashed=bcrypt.hashpw(password.encode('utf-8'),salt)
   #return pwd_context.hash(password)
    return hashed.decode('utf-8') 

def verify_password(password: str, hashed: str) -> bool:
    #return pwd_context.verify(password, hashed)
    return bcrypt.checkpw(password.encode('utf-8'),hashed.encode('utf-8'))


if __name__=="__main__":

    password="inicio2026"

    hashed=hash_password(password)

    print(f"password generate: {hashed}")

    is_valid=verify_password("inicio2026",hashed)

    print(f"password is valid: {is_valid}")