from app.db import get_connection,release_connection
from datetime import datetime
from psycopg.rows import dict_row

def blacklist_token(jti:str,expires_at:datetime)->dict:
    conn=get_connection()
    cur=conn.cursor(row_factory=dict_row)
    try:
        cur.execute(
            """
            INSERT INTO blacklisted_tokens(jti,expires_at)
            VALUES(%s,%s)
            RETURNING jti,expires_at
            """,
            (jti,expires_at)
        )
        blacklisted_token=cur.fetchone()
        conn.commit()
        return blacklisted_token
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        release_connection(conn)

def get_blacklisted_token(jti:str)->dict:
    conn=get_connection()
    cur=conn.cursor(row_factory=dict_row)
    try:
        cur.execute(
            """
             SELECT jti,expires_at FROM blacklisted_tokens
             WHERE jti=%s
            """,
            (jti,)
        )
        blacklisted_token=cur.fetchone()
        return blacklisted_token
    finally:
        cur.close()
        release_connection(conn)