async function shorten() {
    const url = document.getElementById("urlInput").value;

    const res = await fetch("http://localhost:5000/shorten", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url})
    });

    const data = await res.json();

    document.getElementById("result").innerText = data.short_url;
}