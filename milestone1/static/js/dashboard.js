// Renders all charts on the Dashboard page: trends line, market share
// doughnut, and revenue bar chart. Each block guards for its own canvas
// so this file is safe to include even if only some charts are present.

document.addEventListener("DOMContentLoaded", () => {
  if (typeof Chart === "undefined") return;

  const PALETTE = ["#7C5CFC", "#FF6B5B", "#1F8A82", "#E8A33D"];

  // ---- Market Trends (line) ----------------------------------------
  const trendsCanvas = document.getElementById("trendsChart");
  if (trendsCanvas) {
    const years = JSON.parse(trendsCanvas.dataset.years || "[]");
    const values = JSON.parse(trendsCanvas.dataset.values || "[]");

    new Chart(trendsCanvas, {
      type: "line",
      data: {
        labels: years,
        datasets: [
          {
            label: "Market size ($B)",
            data: values,
            borderColor: "#7C5CFC",
            backgroundColor: "rgba(124, 92, 252, 0.12)",
            borderWidth: 2,
            pointBackgroundColor: "#7C5CFC",
            pointRadius: 3,
            tension: 0.35,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#5B6472", font: { family: "IBM Plex Mono", size: 11 } },
          },
          y: {
            grid: { color: "#DEE3E7" },
            ticks: {
              color: "#5B6472",
              font: { family: "IBM Plex Mono", size: 11 },
              callback: (v) => "$" + v + "B",
            },
          },
        },
      },
    });
  }

  // ---- Market Share (doughnut) --------------------------------------
  const shareCanvas = document.getElementById("shareChart");
  if (shareCanvas) {
    const labels = JSON.parse(shareCanvas.dataset.labels || "[]");
    const shares = JSON.parse(shareCanvas.dataset.shares || "[]");
    const remainder = Math.max(0, 100 - shares.reduce((a, b) => a + b, 0));

    new Chart(shareCanvas, {
      type: "doughnut",
      data: {
        labels: [...labels, "Other"],
        datasets: [
          {
            data: [...shares, remainder],
            backgroundColor: [...PALETTE.slice(0, labels.length), "#DEE3E7"],
            borderColor: "#FFFFFF",
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        cutout: "62%",
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: "#5B6472",
              font: { family: "Inter", size: 11.5 },
              boxWidth: 10,
              padding: 12,
            },
          },
        },
      },
    });
  }

  // ---- Revenue by competitor (bar) -----------------------------------
  const revenueCanvas = document.getElementById("revenueChart");
  if (revenueCanvas) {
    const labels = JSON.parse(revenueCanvas.dataset.labels || "[]");
    const revenue = JSON.parse(revenueCanvas.dataset.revenue || "[]");

    new Chart(revenueCanvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Revenue ($M)",
            data: revenue,
            backgroundColor: PALETTE.slice(0, labels.length),
            borderRadius: 6,
            maxBarThickness: 42,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#5B6472", font: { family: "Inter", size: 11 } },
          },
          y: {
            grid: { color: "#DEE3E7" },
            ticks: {
              color: "#5B6472",
              font: { family: "IBM Plex Mono", size: 11 },
              callback: (v) => "$" + v + "M",
            },
          },
        },
      },
    });
  }
});
