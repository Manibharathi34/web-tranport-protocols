import threading
from flask import Blueprint, Response, request
import queue
import time

sse_bp = Blueprint('sse', __name__)

sse_messages = queue.Queue()
event_id = 0
recent_events = []

MAX_RECENT = 100
HEARTBEAT_INTERVAL = 15  # seconds

# Track per-client queues and active connections
client_queues = {}
client_lock = threading.Lock()

# Background message generator
def message_generator(target_queue, prefix):
    i = 0
    while True:
        msg = f"{prefix} Message {i}"
        target_queue.put(msg)
        i += 1
        time.sleep(5)

threading.Thread(target=message_generator, args=(sse_messages, "SSE"), daemon=True).start()

@sse_bp.route('/events')
def sse():
    def event_stream(last_id):
        global event_id

        # Replay missed events if reconnect
        for eid, msg in recent_events:
            if last_id is not None and eid > last_id:
                yield f"id: {eid}\ndata: {msg}\n\n"

        last_heartbeat = time.time()
        while True:
            try:
                msg = sse_messages.get(timeout=1)
                event_id += 1
                recent_events.append((event_id, msg))
                if len(recent_events) > MAX_RECENT:
                    recent_events.pop(0)
                yield f"id: {event_id}\ndata: {msg}\n\n"
            except queue.Empty:
                # Send heartbeat every 15 seconds
                now = time.time()
                if now - last_heartbeat > HEARTBEAT_INTERVAL:
                    yield f"event: heartbeat\ndata: 💓\n\n"
                    last_heartbeat = now

    last_id_header = request.headers.get("Last-Event-ID")
    try:
        last_id = int(last_id_header) if last_id_header else None
    except ValueError:
        last_id = None

    return Response(event_stream(last_id), mimetype="text/event-stream")


@sse_bp.route("/followsse")
def follow_sse():
    client_id = str(uuid.uuid4())
    q = Queue()
    
    with client_lock:
        client_queues[client_id] = q

    def event_stream():
        try:
            while True:
                event_type, msg = q.get()
                yield f"event: {event_type}\ndata: {msg}\n\n"
        except GeneratorExit:
            with client_lock:
                del client_queues[client_id]

    return Response(event_stream(), mimetype="text/event-stream")



@sse_bp.route("/send")
def send():
    is_admin = request.args.get("admin")
    if not is_admin:
        return "Forbidden", 403
    
    message = request.args.get("msg", "hello there!!")
    event_type = request.args.get("event", "update")
    
    with client_lock:
        for cid, q in client_queues.items():
            q.put((event_type, message))
    return "Sent"


@sse_bp.route("/stop")
def stop():
    client_id = request.args.get("id")
    with client_lock:
        if client_id in client_queues:
            client_queues.pop(client_id, None)
            print(f"Client {client_id} manually stopped")
            return f"Stopped client {client_id}", 200
    return "Client not found", 404