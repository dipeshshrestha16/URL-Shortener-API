let chart;

async function loadAnalytics() {
    const res = await fetch("http://127.0.0.1:5000/analytics");
    const urls = await res.json();

    const select = document.getElementById("urlSelect");
    select.innerHTML = "";

    urls.forEach(u => {
        const option = document.createElement("option");
        option.value = u.code;
        option.text = u.long_url;
        select.appendChild(option);
    });

    if (urls.length > 0) {
        updateChart(urls[0].code);
    }
}

async function updateChart(code) {
    const res = await fetch("http://127.0.0.1:5000/analytics");
    const urls = await res.json();

    const urlData = urls.find(u => u.code === code);
    if (!urlData) return;

    const now = Date.now() / 1000;
    const last7 = Array(7).fill(0);

    urlData.click_times.forEach(t => {
        const d = Math.floor((now - t) / 86400);
        if (d < 7) last7[6 - d]++;
    });

    const ctx = document.getElementById("clickChart").getContext("2d");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["6d","5d","4d","3d","2d","Y","T"],
            datasets: [{
                label: 'Clicks',
                data: last7
            }]
        }
    });
}