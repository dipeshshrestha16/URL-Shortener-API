let countdownInterval;

async function shorten() {
    const url = document.getElementById("urlInput").value.trim();

        if (!url) {
            alert("Please enter a URL");
            return;
        }

    const res = await fetch("http://127.0.0.1:5000/shorten", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ url })
    });

    const data = await res.json();

    if (res.status === 429) {
        showRateLimit(data.retry_after);
        return;
    }

    document.getElementById("successBox").classList.remove("hidden");
    document.getElementById("shortUrl").innerText = data.short_url;
}

function showRateLimit(seconds) {
    const box = document.getElementById("rateLimitBox");
    const countdown = document.getElementById("countdown");

    box.classList.remove("hidden");

    let timeLeft = seconds;
    countdown.innerText = timeLeft;

    clearInterval(countdownInterval);

    countdownInterval = setInterval(() => {
        timeLeft--;
        countdown.innerText = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            box.classList.add("hidden");
        }
    }, 1000);
}