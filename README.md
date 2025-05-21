# Real-Time Messaging Demo: Long Polling & Server-Sent Events (SSE)

This project demonstrates how to implement **real-time communication** in a web application using:

- ✅ Long Polling
- ✅ Server-Sent Events (SSE)
- ✅ Python (Flask) backend
- ✅ JavaScript frontend
- ✅ Heartbeats and reconnect logic
- ✅ Multi-tab safe design

---

## 📂 Project Structure
```
web-transport-protocols/
├── routes/
│   ├── __init__.py       # contains create_app()
│   ├── sse.py            # SSE Blueprint
│   ├── longpoll.py       # Long Poll Blueprint
├── static/
│   ├── sse.js
│   └── longpoll.js
├── templates/
│   └── index.html        # Main UI template
├── run.py                # Entry point
└── requirements.txt
```
---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- `pip` installed

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the server
``` bash
python app.py
```

## 🧠 Features
### 🔁 Long Polling
- Client polls /poll endpoint and waits until a message is available.
- Server holds the connection open until a message or timeout.
- Supports message history and clean disconnection.

### 📡 Server-Sent Events (SSE)
- Client connects to /events with EventSource.
- Server pushes events using text/event-stream.
- Includes heartbeat messages every 15 seconds.
- Handles automatic reconnect with id and Last-Event-ID.


## 🧪 How to Test

### Multi-tab scenario

1. **Open** [http://localhost:5000](http://localhost:5000) in two browser tabs.
2. **Use** the "Start Long Polling" or "Start SSE" buttons.
3. **Observe** the following:
   - Messages are pushed every few seconds.
   - **Message ID tracking**
   - **Heartbeats** (♥)
   - **Tab-specific behavior**
   - **Reconnects on server restart**


## 🛠️ Endpoints

| Method | Path      | Description                        |
|--------|-----------|------------------------------------|
| GET    | `/`       | Loads main UI                      |
| GET    | `/poll`   | Long polling endpoint              |
| POST   | `/send`   | Trigger message to long pollers    |
| GET    | `/events` | SSE endpoint (streaming)           |


## 🔄 Advanced Features

- **Heartbeat Support:**  
  Keeps connections alive with periodic empty messages.

- **Reconnect Logic:**  
  SSE automatically retries after disconnects.

- **Multiple Message Channels:**  
  Separate generators for long polling and SSE.


## 🧹 Clean Shutdown

To stop the server:
``` 
CTRL + C
```

## To restart on a new port (if 5000 is busy):
```
python app.py --port 5050
```

## 📌 TODO / Extensions

- [ ] Add WebSocket implementation  
- [ ] Add QUIC support  
- [ ] Auth & session awareness  
- [ ] Persistent message history (Redis, DB)


## 📃 License

MIT License — Free to use and modify.


## 🤝 Acknowledgments

Built using:

- Flask
- Vanilla JavaScript
- EventSource API

