from app.repositories.user_repository import register_repository,login_repository,get_me_repository
from app.utils.auth import hash_password,verify_password,create_access_token

def register_service(user_name:str,email:str,password:str)->dict:
    hashed_password=hash_password(password)
    return register_repository(user_name,email,hashed_password)


def login_service(identifier:str,password:str)->dict:
    user=login_repository(identifier)
    if not user:
        raise ValueError("Invalid credentials")
    correct_password=verify_password(password,user.get("hashed_password"))
    if not correct_password:
        raise ValueError("Invalid credentials")
    access_token=create_access_token({
        "user_id":user.get("id")
    })
    return access_token,user

def get_me_service(user_id:str)->dict:
    return get_me_repository(user_id)