from flask import Blueprint, render_template
from flask_socketio import emit
from routes import socketio
import time

ws_bp = Blueprint('websocket', __name__)

@ws_bp.route("/websocket")
def websocket_ui():
    return render_template("ws.html")  # We'll create this next

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Connected to WebSocket!'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('send_message')
def handle_message(data):
    print(f"Received message: {data}")
    res = f" received on server - {data['message']} - on time {time.time()}"
    emit('message', {'data': res}, broadcast=True)
