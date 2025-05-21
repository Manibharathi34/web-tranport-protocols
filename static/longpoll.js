let pollRunning = false;

function startLongPoll() {
    pollRunning = true;
    poll();
}

function stopLongPoll() {
    pollRunning = false;
}

function poll() {
    if (!pollRunning) return;
    fetch('/lp/longpoll')
        .then(response => {
            if (response.status === 204) return { message: "No new message (timeout)" };
            return response.json();
        })
        .then(data => {
            const li = document.createElement("li");
            li.textContent = `[LongPoll] ${data.message}`;
            document.getElementById("longpoll-output").appendChild(li);
            if (pollRunning) poll();
        })
        .catch(err => {
            console.error("Polling error", err);
            setTimeout(poll, 3000);
        });
}
