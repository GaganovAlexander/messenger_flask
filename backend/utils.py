from hashlib import sha256
from datetime import datetime
from random import randint

from psycopg2.errors import UniqueViolation

from backend.db.authorization import add_token


def generate_autorization_token(username, password_hash):
    auth_token = sha256((username + password_hash + str(datetime.now()) + str(randint(-256, 255))).encode('utf-8')).hexdigest()
    try:
        add_token(username, auth_token)
        return auth_token
    except UniqueViolation:
        generate_autorization_token(username, password_hash)

def hash_password(password: str):
    return sha256(password.encode('utf-8')).hexdigest()
