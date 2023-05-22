from flask import request, jsonify

from configs import MAIN_ROUTE
from backend import app
import backend.db as db


@app.route(MAIN_ROUTE + '/chat', methods=['PUT', 'PATCH', 'DELETE', 'GET'])
def chat():
    method = request.method
    data = request.json
    users = data.get('users')
    chat_id = data.get('chat_id')
    user_id = db.authorization.get_user_id(request.headers.get('authorization-token'))

    if method == 'PUT':
        users.append(user_id)
        id = db.chats.create(list(set(users)))
        return {'status': 0, 'id': id}
    
    elif method == 'PATCH':
        db.chats.add_users(chat_id, users)
    elif method == 'DELETE':
        db.chats.delete(chat_id)
    elif method == 'GET':
        return jsonify(db.messages.get_top100_chat_messages(chat_id))

    return {'status': 0}, 200

@app.route(MAIN_ROUTE + '/messages', methods=['PUT', 'PATCH', 'DELETE'])
def messeges():
    ...