from psycopg_pool import ConnectionPool
from app.config import settings

connection_pool=ConnectionPool(
    min_size=1,
    max_size=20,
    kwargs={
        "port":settings.DB_PORT,
        "dbname":settings.DB_NAME,
        "password":settings.DB_PASSWORD,
        "user":settings.DB_USER,
        "host":settings.DB_HOST
    }
)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    return connection_pool.putconn(conn)