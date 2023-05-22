from datetime import datetime

from backend.db import conn, cur


def add_to_chat(chat_id: int, user_id: int, message: str):
    cur.execute('''INSERT INTO messages(chat_id, sender, created_at, message) 
                   VALUES(%s, %s, %s, %s)''', (chat_id, user_id, datetime.now(), message))
    conn.commit()

def delete(message_id: int):
    cur.execute('DELETE FROM messages WHERE id = %s', (message_id,))
    conn.commit()

def change(message_id: int, new_message: str):
    cur.execute('UPDATE messages SET message = %s WHERE id = %s',
                (new_message, message_id))

def get_top100_chat_messages(chat_id: int):
    cur.execute('''SELECT * FROM messages WHERE chat_id = %s 
                   ORGER BY created_at LIMIT 100''', (chat_id,))
    return cur.fetchall()
