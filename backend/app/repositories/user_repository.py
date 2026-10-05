from app.db import get_connection,release_connection
from psycopg.rows import dict_row

def register_repository(user_name:str,email:str,hashed_password:str)->dict:
        conn=get_connection()
        cur=conn.cursor(row_factory=dict_row)
        try:
            cur.execute(
            """
                INSERT INTO users(user_name,email,hashed_password)
                VALUES(%s,%s,%s)
                RETURNING id,user_name,email 
            """,
                (user_name,email,hashed_password)
            )
            user=cur.fetchone()
            conn.commit()
            return user
        except Exception:
              conn.rollback()
              raise
        finally:
              cur.close()
              release_connection(conn)

def login_repository(identifier:str)->dict:
    conn=get_connection()
    cur=conn.cursor(row_factory=dict_row)
    try:
        cur.execute(
        """
            SELECT id,user_name,email,hashed_password FROM users
            WHERE user_name=%s OR email=%s
        """,
        (identifier,identifier)
        )
        user=cur.fetchone()
        return user
    finally:
         cur.close()
         release_connection(conn)

def get_me_repository(user_id:int)->dict:
    conn=get_connection()
    cur=conn.cursor(row_factory=dict_row)
    try:
        cur.execute(
        """
            SELECT id,user_name,email FROM users
            WHERE id=%s
        """,
        (user_id,)
        )
        user=cur.fetchone()
        return user
    finally:
        cur.close()
        release_connection(conn)

      
            
