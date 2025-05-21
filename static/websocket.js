let socket = null;

function startWebSocket() {
    const log = document.getElementById("ws-log");
    log.innerHTML = "🔌 Connecting to WebSocket...\n";

    socket = io("/ws");  // matches the blueprint prefix `/ws`

    socket.on("connect", () => {
        log.innerHTML += "✅ WebSocket connected\n";
    });

    socket.on("message", (data) => {
        log.innerHTML += `📨 Message: ${data}\n`;
    });

    socket.on("disconnect", () => {
        log.innerHTML += "❌ WebSocket disconnected\n";
    });
}

function stopWebSocket() {
    if (socket) {
        socket.disconnect();
        document.getElementById("ws-log").innerHTML += "🛑 WebSocket disconnected manually\n";
    }
}

function sendWSMessage() {
    if (socket) {
        socket.emit("message", "Hello from WebSocket client!");
    }
}

document.getElementById("ws-start-btn").addEventListener("click", startWebSocket);
document.getElementById("ws-stop-btn").addEventListener("click", stopWebSocket);
document.getElementById("ws-send-btn").addEventListener("click", sendWSMessage);
