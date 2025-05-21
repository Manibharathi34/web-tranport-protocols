let evtSource = null;

function startSSE() {
    if (evtSource) {
        console.log("SSE already running");
        return;
    }

    evtSource = new EventSource('/sse/events');

    evtSource.onopen = () => {
        console.log("✅ SSE connection opened.");
        appendLog("SSE connected.");
    };

    evtSource.onerror = (err) => {
        console.error("❌ SSE error:", err);
        appendLog("SSE error or disconnected.");
    };

    // Default handler for 'message' events
    evtSource.onmessage = (event) => {
        appendMessage("default", event.data);
    };

    // Custom event: 'update'
    evtSource.addEventListener('update', function (event) {
        appendMessage("update", event.data);
    });

    // Custom event: 'notice'
    evtSource.addEventListener('notice', function (event) {
        appendMessage("notice", event.data);
    });

    // Heartbeat handling
    evtSource.addEventListener('heartbeat', function (event) {
        console.log("💓 Heartbeat received.");
        appendMessage("hearbeat", "💓 Heartbeat received.");
    });
}

function stopSSE() {
    if (evtSource) {
        evtSource.close();
        appendLog("SSE stopped.");
        console.log("SSE connection closed.");
        evtSource = null;
    }
}

function appendMessage(type, msg) {
    const container = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = "message " + type;
    div.textContent = `[${type}] ${msg}`;
    container.appendChild(div);
}

function appendLog(msg) {
    const log = document.getElementById("log");
    const entry = document.createElement("div");
    entry.className = "log-entry";
    entry.textContent = msg;
    log.appendChild(entry);
}
