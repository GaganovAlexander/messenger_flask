from backend.db import conn, cur

from psycopg2 import Binary


def create(username: str, password_hash: str, nickname: str) -> None:
    cur.execute("INSERT INTO users (username, password_hash, nickname) VALUES (%s, %s, %s)", 
                (username, password_hash, nickname))
    conn.commit()

def get_all():
    cur.execute('SELECT id, nickname FROM users')
    return cur.fetchall()

def get_by_username(username: str) -> dict:
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cur.fetchone()

def get_by_id(user_id: str) -> dict:
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cur.fetchone()

def delete(user_id: str) -> None:
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

def change_auth_params(user_id: str, new_username: str, new_password) -> None:
    cur.execute("UPDATE users SET username = %s, password_hash = %s WHERE id = %s",
                (new_username, new_password, user_id))
    conn.commit()

def add_profile_item(user_id: int, item_name, item) -> None:
    if item_name == 'picture':
        item = Binary(item)
    cur.execute(f"UPDATE users SET {item_name} = %s WHERE id = %s", (item, user_id))
    conn.commit()
    