from flask_socketio import send

from backend import socketio


@socketio.on('message')
def handle_message(data):
    send(data, broadcast=True)
    