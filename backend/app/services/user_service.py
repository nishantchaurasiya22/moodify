from app.repositories.user_repository import register_repository,login_repository
from app.utils.auth import hash_password,verify_password,create_access_token
def register_services(user_name:str,email:str,password:str)->dict:
    hashed_password=hash_password(password)
    return register_repository(user_name,email,hashed_password)


def login_service(identifier,password)->dict:
    user=login_repository(identifier)
    if not user:
        raise ValueError("Invalid Credentials")
    correct_password=verify_password(password,user["hashed_password"])
    if not correct_password:
        raise ValueError("Invalid Credentials")
    access_token=create_access_token({
        "user_id":user["id"]
    })
    return access_token,user
    