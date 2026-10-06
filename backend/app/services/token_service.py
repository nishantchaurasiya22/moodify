from app.repositories.token_repository import blacklist_token,get_blacklisted_token
from datetime import datetime,timezone


def blacklist_token_service(payload:dict)->dict:
    expires_at=datetime.fromtimestamp(payload.get("exp"),tz=timezone.utc)
    jti=payload.get("jti")
    return blacklist_token(jti,expires_at)

def get_blacklisted_token_service(jti:str)->dict:
    return get_blacklisted_token(jti)