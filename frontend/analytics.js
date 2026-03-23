// load all URLs into dropdown
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

    if(urls.length > 0){
        updateChart(urls[0].code);
    }
}

// update chart for selected URL
async function updateChart(code) {
    const res = await fetch("http://127.0.0.1:5000/analytics");
    const urls = await res.json();
    const urlData = urls.find(u => u.code === code);

    if(!urlData) return;

    const now = Date.now() / 1000;
    const last7Days = Array(7).fill(0);

    (urlData.click_times || []).forEach(t => {
        const diffDays = Math.floor((now - t) / 86400);
        if(diffDays < 7) last7Days[6 - diffDays]++;
    });

    const ctx = document.getElementById("clickChart").getContext("2d");
    if(chart) chart.destroy();

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["6 days ago","5 days ago","4 days ago","3 days ago","2 days ago","Yesterday","Today"],
            datasets: [{
                label: 'Clicks',
                data: last7Days,
                borderColor: 'blue',
                fill: false,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, precision: 0 }
            }
        }
    });
}

// event listeners
document.getElementById("urlSelect").addEventListener("change", e => {
    updateChart(e.target.value);
});

function refreshAnalytics() {
    loadAnalytics();
}

// initial load
loadAnalytics();