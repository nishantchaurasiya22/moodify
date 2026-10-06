from fastapi import Request,HTTPException,status
from app.utils.auth import verify_token
from app.services.token_service import get_blacklisted_token_service

async def get_current_user(request:Request)->dict:
    token=request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Login required")
    payload=verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized user")
    jti=payload.get("jti")
    if not jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    blacklisted_token = await get_blacklisted_token_service(jti)
    if blacklisted_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token blacklisted")
    return payload
    
