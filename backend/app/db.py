from psycopg_pool import AsyncConnectionPool
from app.config import settings

connection_pool=AsyncConnectionPool(
    min_size=1,
    max_size=20,
    open=False,
    kwargs=({
        "dbname":settings.DB_NAME,
        "port":settings.DB_PORT,
        "password":settings.DB_PASSWORD,
        "user":settings.DB_USER,
        "host":settings.DB_HOST
    })
)

async def get_connection():
    return await connection_pool.getconn()

async def release_connection(conn):
    return await connection_pool.putconn(conn)