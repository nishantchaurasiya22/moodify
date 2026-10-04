from fastapi import APIRouter,status,HTTPException,Response,Depends
from psycopg.errors import UniqueViolation
from app.dependencies import get_current_user
from app.dtos.user import ResponseUser,CreateUser,LoginCreate
from app.services.user_service import register_services,login_service,get_me_service
auth_router=APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register",response_model=ResponseUser,status_code=status.HTTP_201_CREATED)
def register(user:CreateUser):
    try:
        return register_services(user.user_name,user.email,user.password)
    except UniqueViolation:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exist")

@auth_router.post("/login",response_model=ResponseUser,status_code=status.HTTP_200_OK)
def login(user:LoginCreate,response:Response):
    try:
        access_token,user_data=login_service(user.identifier,user.password)
        response.set_cookie(
            key="access_token",
            value=access_token,
            samesite="lax",
            httponly=True,
            secure=False
        )
        return user_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))

@auth_router.get("/me",response_model=ResponseUser,status_code=status.HTTP_200_OK)
def get_me(current_user:dict=Depends(get_current_user)):
    user_id=int(current_user.get("sub"))
    user=get_me_service(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user