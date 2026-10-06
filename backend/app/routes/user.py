from fastapi import APIRouter,status,HTTPException,Depends,Response,Request
import psycopg
from app.services.user_service import register_service,login_service,get_me_service
from app.dtos.user import CreateUser,ResponseUser,LoginUser
from app.dependencies import get_current_user
auth_router=APIRouter(prefix="/auth",tags=["auth"])

@auth_router.post("/register",response_model=ResponseUser,status_code=status.HTTP_201_CREATED)
async def register(user:CreateUser):
    try:
        return await register_service(user.user_name.strip().lower(),user.email.lower(),user.password)
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exist")

@auth_router.post("/login",response_model=ResponseUser,status_code=status.HTTP_200_OK)
async def login(user:LoginUser,response:Response):
    try:
        to_encode,user_data=await login_service(user.identifier.strip().lower(),user.password)
        response.set_cookie(
            key="access_token",
            value=to_encode,
            samesite="lax",
            httponly=True,
            secure=False
        )
        return user_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))


@auth_router.get("/me",response_model=ResponseUser,status_code=status.HTTP_200_OK)
async def get_me(current_user:dict=Depends(get_current_user)):
    user_id=int(current_user.get("sub"))
    user=await get_me_service(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user



    
