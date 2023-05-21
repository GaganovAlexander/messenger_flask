from backend.db import conn, cur 
from backend.db.users import get_by_username

def add_token(username: str, token: str) -> None:
    user = get_by_username(username)
    cur.execute("INSERT INTO authorizations (user_id, authorization_token) VALUES (%s, %s)", (user.get("id"), token))
    conn.commit()

def get_user_id(auth_token: str) -> int:
    cur.execute("SELECT user_id FROM authorizations WHERE authorization_token = %s", (auth_token,))
    data = cur.fetchone()
    return data.get("user_id") if data else None

def delete_auths(user_id: str, auth_token: str) -> None:
    cur.execute("DELETE FROM authorizations WHERE user_id = %s AND authorization_token <> %s", (user_id, auth_token))
    conn.commit()