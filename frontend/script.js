async function shorten() {
    console.log("Button clicked");
    const url = document.getElementById("urlInput").value;
    console.log("sending request...");

    if (!url){
        alert("Please enter a URL");
        return;
    }

    try{
        const res = await fetch("http://localhost:5000/shorten", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({url})
        });

    const data = await res.json();

    document.getElementById("result").innerHTML = `<a href="${data.short_url}" target="_blank">${data.short_url}</a>`;
    } catch (err){
        console.error("Error:", err);
        alert("Something went wrong. Please try again.");
    }
}
