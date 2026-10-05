from fastapi import HTTPException,Request,status
from app.utils.auth import verify_token

def get_current_user(request:Request)->dict:
        token=request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="login required")
        payload=verify_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized user")
        return payload