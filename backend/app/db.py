from psycopg_pool import ConnectionPool
from app.config import settings
from psycopg.rows import dict_row

connection_pool=ConnectionPool(
    min_size=1,
    max_size=20,
    kwargs=({
        "dbname":settings.DB_NAME,
        "port":settings.DB_PORT,
        "password":settings.DB_PASSWORD,
        "user":settings.DB_USER,
        "host":settings.DB_HOST
    })
)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    return connection_pool.putconn(conn)