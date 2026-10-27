from fastapi import APIRouter,HTTPException,status,Depends,Response
from app.services.auth_service import register_service,login_service
from app.dtos.user import ResponseUser,CreateUser,LoginUser
from psycopg.errors import UniqueViolation
from app.config import settings
from app.dependencies import get_current_user
auth_router=APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register",response_model=ResponseUser,status_code=status.HTTP_201_CREATED)
async def register(user:CreateUser):
    try:
        return await register_service(user.user_name.strip().lower(),user.email.strip().lower(),user.password)
    except UniqueViolation:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exist")

@auth_router.post("/login",response_model=ResponseUser,status_code=status.HTTP_200_OK)
async def login(user:LoginUser,response:Response):
    try:
        access_token,user=await login_service(user.identifier.lower().strip(),user.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))
    response.set_cookie(
        value=access_token,
        key="access_token",
        httponly= True,
        secure=False, 
        samesite="lax", 
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return user

@auth_router.get("/me", response_model=ResponseUser)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=True, secure=False, samesite="lax")
    return {"message": "Logged out"}