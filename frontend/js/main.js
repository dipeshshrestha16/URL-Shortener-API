document.getElementById("shortenBtn").addEventListener("click", shorten);

document.getElementById("urlSelect").addEventListener("change", e => {
    updateChart(e.target.value);
});
document.getElementById("copyBtn").addEventListener("click", async () => {
    const text = document.getElementById("shortUrl").innerText;
    try {
        await navigator.clipboard.writeText(text);
        const btn = document.getElementById("copyBtn");
        btn.textContent = "Copied!";
        setTimeout(() => btn.textContent = "Copy", 1500);
    } catch (err) {
        console.error("Failed to copy:", err);
        alert("Failed to copy. Please try manually.");
    }
});

document.getElementById("refreshAllBtn").addEventListener("click", loadAnalytics);

loadAnalytics();