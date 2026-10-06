from app.repositories.token_repository import blacklist_token,get_blacklisted_token
from datetime import datetime,timezone


async def blacklist_token_service(payload:dict)->dict:
    expires_at=datetime.fromtimestamp(payload.get("exp"),tz=timezone.utc)
    jti=payload.get("jti")
    return await blacklist_token(jti,expires_at)

async def get_blacklisted_token_service(jti:str)->dict:
    return await get_blacklisted_token(jti)