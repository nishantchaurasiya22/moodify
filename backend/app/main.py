from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.auth_route import auth_router
from app.db import connection_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connection_pool.open()
    yield
    await connection_pool.close()
app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)