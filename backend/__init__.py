from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

from backend.chats import *
from backend.users import *
from backend.messages import *