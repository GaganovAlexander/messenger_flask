from flask import request, Response

from configs import MAIN_ROUTE
from backend import app
import backend.db as db
from backend.utils import generate_autorization_token, hash_password


@app.route(MAIN_ROUTE + '/user', methods=['PUT', 'POST', 'PATCH', 'DELETE'])
def user():
    method = request.method
    data = request.json
    username = data.get('username')
    password = data.get('password')
    nickname = data.get('nickname')
    user_id = db.authorization.get_user_id(request.headers.get('authorization-token'))

    if method == 'PUT':
        if not (username and password and nickname):
            return {'status': 1, 'error': 'username, password and nickname are required'}, 400
        if db.users.get_by_username(username):
            return {'status': 1, 'error': 'user already exists'}, 400
        password_hash = hash_password(password)
        db.users.create(username, password_hash, nickname)
        auth_token = generate_autorization_token(username, password_hash)
        return {'status': 0, 'autorization_token': auth_token}, 200
        
    elif method == 'POST':
        user = db.users.get_by_username(username)
        password_hash = hash_password(password)
        if user and user.get('password_hash') == password_hash:
            auth_token = generate_autorization_token(username, password_hash)
            return {'status': 0, 'autorization_token': auth_token}, 200
        return {'status': 1, 'error': 'wrong username or password'}, 400
    
    elif method == 'PATCH':
        if user_id:
            new_username = data.get('new_username') if data.get('new_username') else username
            new_password = data.get('new_password')
            if new_password:
                db.authorization.delete_auths(user_id, data.get('autorization_token'))
                new_password = hash_password(new_password)
            else:
                new_password = user.get('password_hash')
            db.users.change_auth_params(user_id, new_username, new_password)
            return {'status': 0}, 200
        return {'status': 1, 'error': 'you are not authorized'}, 400
            
    elif method == 'DELETE':
        if user_id:
            db.users.delete(user_id)
            return {'status': 0}, 200
        return {'status': 1, 'error': 'you are not authorized'}, 400


@app.get(MAIN_ROUTE + '/users')
def users():
    return db.users.get_all()

@app.route(MAIN_ROUTE + '/profile', methods=['PUT', 'GET', 'DELETE'])
def profile():
    user_id = db.authorization.get_user_id(request.headers.get('authorization-token'))
    if not user_id:
        return {'status': 1, 'error': 'you are not authorized'}, 400
    
    valid_items = ['picture', 'age', 'gender', 'description']
    item = request.args.get('item')
    if not item in valid_items:
        return {'status': 1, 'error': f'item {item} is invalid'}
    
    method = request.method

    if item == 'picture' and method != 'DELETE':
        if method == 'PUT':
            file = request.files.get('picture')
            db.users.add_profile_item(user_id, item, file.read())
        elif method == 'GET':
            return Response(db.users.get_by_id(user_id).get('picture'), 200, mimetype='image/png')
        
    else:
        if method == 'PUT':
            db.users.add_profile_item(user_id, item, request.json.get(item))
        elif method == 'GET':
            return {'status': 0, item: db.users.get_by_id(user_id).get(item)}, 200
        elif method == 'DELETE':
            db.users.add_profile_item(user_id, item, None)

    return {'status': 0}, 200