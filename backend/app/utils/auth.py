from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
from app.config import settings
import jwt
password_hash=PasswordHash.recommended()

def hash_password(password:str)->str:
    hashed_password=password_hash.hash(password)
    return hashed_password

def verify_password(password,hashed_password)->bool:
    return password_hash.verify(password,hashed_password)

def create_access_token(data:dict)->str:
    to_encoded=data.copy()
    user_id=to_encoded.get("user_id")
    if not user_id:
        raise ValueError("Login required")
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encoded.update({
        "sub":str(user_id),
        "exp":expire
    })
    jwt_endoded=jwt.encode(
        to_encoded,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return jwt_endoded

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
