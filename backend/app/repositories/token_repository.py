from app.db import get_connection,release_connection
from datetime import datetime
from psycopg.rows import dict_row

async def blacklist_token(jti:str,expires_at:datetime)->dict:
    conn=await get_connection()
    cur=conn.cursor(row_factory=dict_row)
    try:
        await cur.execute(
            """
            INSERT INTO blacklisted_tokens(jti,expires_at)
            VALUES(%s,%s)
            RETURNING jti,expires_at
            """,
            (jti,expires_at)
        )
        blacklisted_token=await cur.fetchone()
        await conn.commit()
        return blacklisted_token
    except Exception:
        await conn.rollback()
        raise
    finally:
        await cur.close()
        await release_connection(conn)

async def get_blacklisted_token(jti:str)->dict:
    conn=await get_connection()
    cur=conn.cursor(row_factory=dict_row)
    try:
        await cur.execute(
            """
             SELECT jti,expires_at FROM blacklisted_tokens
             WHERE jti=%s
            """,
            (jti,)
        )
        blacklisted_token=await cur.fetchone()
        return blacklisted_token
    finally:
        await cur.close()
        await release_connection(conn)