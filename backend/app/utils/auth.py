from pwdlib import PasswordHash
import jwt
import uuid
from app.config import settings
from datetime import datetime,timedelta,timezone
password_hash=PasswordHash.recommended()
def hash_password(password):
    return password_hash.hash(password)

def verify_password(password:str,hashed_password:str)->bool:
    return password_hash.verify(password,hashed_password)


def create_access_token(data:dict)->dict:
    to_encode=data.copy()
    user_id=to_encode.get("user_id")
    if not user_id:
        raise ValueError("Invalid credential")
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "sub":str(user_id),
        "exp":expire,
        "jti":str(uuid.uuid4())
    })
    to_encoded=jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return to_encoded

def verify_token(token:str)->dict:
    try:
        payload=jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
