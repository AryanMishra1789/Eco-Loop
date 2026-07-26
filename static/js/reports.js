document.addEventListener("DOMContentLoaded", () => {

    initializeCharts();

    document
        .getElementById("exportPdf")
        .addEventListener("click", exportPdf);

    document
        .getElementById("exportCsv")
        .addEventListener("click", exportCsv);

    loadReport();

});

let energyChart;
let breakdownChart;

/* ==========================================================
   Charts
========================================================== */

function initializeCharts() {

    energyChart = new Chart(

        document.getElementById("energyReportChart"),

        {

            type: "line",

            data: {

                labels: [],

                datasets: [

                    {

                        label: "Energy Consumption",

                        data: [],

                        borderWidth: 2,

                        tension: .35,

                        fill: false

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false

            }

        }

    );

    breakdownChart = new Chart(

        document.getElementById("breakdownChart"),

        {

            type: "doughnut",

            data: {

                labels: [

                    "Cooling",
                    "Heating",
                    "Lighting",
                    "Equipment"

                ],

                datasets: [

                    {

                        data: [25,25,25,25]

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false

            }

        }

    );

}

/* ==========================================================
   Load Report
========================================================== */

async function loadReport() {

    try {

        /*
            Replace with your backend endpoint.

            Example:

            GET /reports/latest
        */

        const response = await fetch("/reports");

        if (!response.ok) {

            throw new Error();

        }

        const report = await response.json();

        populateReport(report);

    }

    catch (error) {

        console.error(error);

    }

}

/* ==========================================================
   Populate
========================================================== */

function populateReport(report) {

    document.getElementById("totalEnergy").innerText =
        format(report.total_energy);

    document.getElementById("estimatedCost").innerText =
        format(report.estimated_cost);

    document.getElementById("co2Reduction").innerText =
        format(report.co2_reduction);

    document.getElementById("energySavings").innerText =
        format(report.energy_savings);

    document.getElementById("executiveSummary").innerText =
        report.summary || "No executive summary available.";

    populateCharts(report);

    populateTable(report.metrics || {});

}

/* ==========================================================
   Charts
========================================================== */

function populateCharts(report) {

    if (report.energy_history) {

        energyChart.data.labels =

            report.energy_history.map(

                (_, index) => `M${index + 1}`

            );

        energyChart.data.datasets[0].data =

            report.energy_history;

    }

    energyChart.update();

    breakdownChart.data.datasets[0].data = [

        report.cooling || 0,

        report.heating || 0,

        report.lighting || 0,

        report.equipment || 0

    ];

    breakdownChart.update();

}

/* ==========================================================
   Table
========================================================== */

function populateTable(metrics) {

    const table = document.getElementById("reportTable");

    table.innerHTML = "";

    const keys = Object.keys(metrics);

    if (!keys.length) {

        table.innerHTML = `

            <tr>

                <td colspan="3"
                    class="text-center">

                    No report data available.

                </td>

            </tr>

        `;

        return;

    }

    keys.forEach(key => {

        table.insertAdjacentHTML(

            "beforeend",

            `

            <tr>

                <td>${beautify(key)}</td>

                <td>${metrics[key]}</td>

                <td>-</td>

            </tr>

            `

        );

    });

}

/* ==========================================================
   Export
========================================================== */

function exportPdf() {

    /*
        Replace with your backend endpoint

        Example:

        /reports/export/pdf
    */

    window.open(

        "/reports/export/pdf",

        "_blank"

    );

}

function exportCsv() {

    /*
        Replace with your backend endpoint

        Example:

        /reports/export/csv
    */

    window.open(

        "/reports/export/csv",

        "_blank"

    );

}

/* ==========================================================
   Helpers
========================================================== */

function beautify(text) {

    return text

        .replace(/_/g, " ")

        .replace(/\b\w/g, c => c.toUpperCase());

}

function format(value) {

    if (value === undefined ||
        value === null) {

        return "--";

    }

    if (typeof value === "number") {

        return value.toFixed(2);

    }

    return value;

}