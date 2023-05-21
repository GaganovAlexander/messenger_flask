from backend.db import conn, cur


def create(users: list[int]) -> int:
    cur.execute('INSERT INTO chats(users) VALUES(%s) RETURNING id', (users,))
    conn.commit()
    return cur.fetchone().get('id')

def add_users(chat_id: int, users: list[str]):
    cur.execute('SELECT users FROM chat WHERE id = %s', (chat_id,))
    users.extend(cur.fetchone().get('users'))
    cur.execute('UPDATE chat SET users = %s WHERE id = %s', (list(set(users)), chat_id))
    conn.commit()

def delete(chat_id):
    cur.execute('DELETE FROM chat WHERE id = %s', (chat_id,))
    conn.commit()