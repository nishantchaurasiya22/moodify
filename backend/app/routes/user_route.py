from fastapi import APIRouter,status,HTTPException,Response
from psycopg.errors import UniqueViolation
from app.dtos.user import ResponseUser,CreateUser,LoginCreate
from app.services.user_service import register_services,login_service
auth_router=APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register",response_model=ResponseUser,status_code=status.HTTP_201_CREATED)
def register(user:CreateUser):
    try:
        return register_services(user.user_name,user.email,user.password)
    except UniqueViolation:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exist")

@auth_router.post("/login",response_model=ResponseUser)
def login(user:LoginCreate,response:Response):
    try:
        access_token,user_data=login_service(user.identifier,user.password)
        response.set_cookie(
            key="acesss_token",
            value=access_token,
            samesite="lax",
            secure=False,
            httponly=True
        )
        return user_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_200_OK,detail=str(e))