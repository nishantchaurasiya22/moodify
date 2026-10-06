from fastapi import FastAPI
from app.routes.user import auth_router
from app.routes.token import token_router
app=FastAPI()

app.include_router(auth_router)
app.include_router(token_router)