from fastapi import APIRouter,status,Response,Depends
from app.services.token_service import blacklist_token_service
from app.dependencies import get_current_user
token_router=APIRouter(prefix="/token",tags=["token"])

@token_router.post("/logout",response_model=None)
def logout(response:Response,current_user:dict=Depends(get_current_user)):
    blacklist_token_service(current_user)
    response.delete_cookie(
        key="access_token",
        samesite="lax",
        httponly=True,
        secure=False
    )
    return None

