from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import connection_pool
from app.routes.user import auth_router
from app.routes.token import token_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connection_pool.open()
    yield
    await connection_pool.close()
app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(token_router)



