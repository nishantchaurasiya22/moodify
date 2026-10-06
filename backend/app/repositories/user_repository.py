from app.db import get_connection,release_connection
from psycopg.rows import dict_row

async def register_repository(user_name:str,email:str,hashed_password:str)->dict:
    conn=await get_connection()
    cur=conn.cursor(row_factory=dict_row)
    try:
        await cur.execute(
            """ 
             INSERT INTO users(user_name,email,hashed_password)
             VALUES(%s,%s,%s)
             RETURNING id,user_name,email,created_at,updated_at
            """,
            (user_name,email,hashed_password)
        )
        user=await cur.fetchone()
        await conn.commit()
        return user
    except Exception:
        await conn.rollback()
        raise
    finally:
        await cur.close()
        await release_connection(conn)

async def login_repository(identifier:str)->dict:
    conn=await get_connection()
    cur=conn.cursor(row_factory=dict_row)
    try:
        await cur.execute(
            """
            SELECT id,user_name,email,hashed_password,created_at,updated_at FROM users
            WHERE user_name=%s OR email=%s
            """,
            (identifier,identifier)
        )
        user=await cur.fetchone()
        return user
    finally:
        await cur.close()
        await release_connection(conn)

async def get_me_repository(user_id:str)->dict:
    conn=await get_connection()
    cur=conn.cursor(row_factory=dict_row)
    try:
        await cur.execute(
            """
            SELECT id,user_name,email,created_at,updated_at FROM users
            WHERE id=%s
            """,
            (user_id,)
        )
        user=await cur.fetchone()
        return user
    finally:
        await cur.close()
        await release_connection(conn)

