from fastapi import Request,HTTPException,status
from app.services.auth_service import get_me_service
from app.utils.auth import verify_token

async def get_current_user(request:Request)->dict:
    token=request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Login required")
    payload=verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized user")
    user=await get_me_service(int(payload.get("sub")))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized user")
    return user
        
