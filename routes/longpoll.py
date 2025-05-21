import threading
from flask import Blueprint, Response, jsonify, render_template, request
import queue
import time

longpoll_bp = Blueprint('longpoll', __name__)
longpoll_messages = queue.Queue()


# Background message generator
def message_generator(target_queue, prefix):
    i = 0
    while True:
        msg = f"{prefix} Message {i}"
        target_queue.put(msg)
        i += 1
        time.sleep(5)

threading.Thread(target=message_generator, args=(longpoll_messages, "LP"), daemon=True).start()


@longpoll_bp.route("/longpoll")
def long_poll():
    try:
        msg = longpoll_messages.get(timeout=30)
        return jsonify({"message": msg})
    except queue.Empty:
        return jsonify({"message": "timeout"}), 204
