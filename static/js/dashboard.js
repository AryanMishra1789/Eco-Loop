document.addEventListener("DOMContentLoaded", () => {

    initializeCharts();

    document
        .getElementById("runSimulation")
        .addEventListener("click", runSimulation);

});

let energyChart;
let distributionChart;

/* ==========================================================
   Initialize Charts
========================================================== */

function initializeCharts() {

    const energyCtx = document
        .getElementById("energyChart")
        .getContext("2d");

    energyChart = new Chart(energyCtx, {

        type: "line",

        data: {

            labels: [],

            datasets: [

                {

                    label: "Energy Consumption",

                    data: [],

                    borderWidth: 2,

                    tension: 0.3,

                    fill: false

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

    const distributionCtx = document
        .getElementById("distributionChart")
        .getContext("2d");

    distributionChart = new Chart(distributionCtx, {

        type: "doughnut",

        data: {

            labels: [

                "Cooling",
                "Heating",
                "Lighting",
                "Other"

            ],

            datasets: [

                {

                    data: [25, 25, 25, 25]

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}

/* ==========================================================
   Run Simulation
========================================================== */

async function runSimulation() {

    const button = document.getElementById("runSimulation");

    button.disabled = true;
    button.innerText = "Running Simulation...";

    try {

        const building = document
            .getElementById("buildingName")
            .value;

        const response = await fetch("/api/agent/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                message: `Run energy simulation for ${building}`

            })

        });

        if (!response.ok) {

            throw new Error("Simulation failed.");

        }

        const result = await response.json();

        processSimulationResult(result);

        alert("Simulation completed successfully!");

    }

    catch (error) {

        console.error(error);

        alert("Unable to complete simulation.");

    }

    finally {

        button.disabled = false;

        button.innerText = "Run Simulation";

    }

}

/* ==========================================================
   Process Result
========================================================== */

function processSimulationResult(response) {

    if (
        !response.tool_result ||
        !response.tool_result.result
    ) {

        alert("Simulation completed but returned no data.");

        return;

    }

    const result = response.tool_result.result;

    const metrics = result.metrics || {};

    updateKPIs(metrics);

    updateCharts(metrics);

    updateRecommendations(

        result.recommendations || []

    );

    addHistory(metrics);

}

/* ==========================================================
   KPI Cards
========================================================== */

function updateKPIs(metrics) {

    document.getElementById("energyValue").innerText =
        formatValue(metrics.energy_consumption);

    document.getElementById("hvacValue").innerText =
        formatValue(metrics.hvac_load);

    document.getElementById("temperatureValue").innerText =
        formatValue(metrics.indoor_temperature);

    document.getElementById("co2Value").innerText =
        formatValue(metrics.co2_emissions);

}

/* ==========================================================
   Charts
========================================================== */

function updateCharts(metrics) {

    energyChart.data.labels = [

        "Cooling",
        "Heating",
        "Lighting",
        "HVAC"

    ];

    energyChart.data.datasets[0].data = [

        metrics.cooling_load || 0,
        metrics.heating_load || 0,
        metrics.lighting_load || 0,
        metrics.hvac_load || 0

    ];

    energyChart.update();

    distributionChart.data.datasets[0].data = [

        metrics.cooling_load || 0,
        metrics.heating_load || 0,
        metrics.lighting_load || 0,
        Math.max(
            0,
            (metrics.energy_consumption || 0)
            -
            (metrics.cooling_load || 0)
            -
            (metrics.heating_load || 0)
            -
            (metrics.lighting_load || 0)
        )

    ];

    distributionChart.update();

}

/* ==========================================================
   Recommendations
========================================================== */

function updateRecommendations(recommendations) {

    const table =
        document.getElementById("recommendationTable");

    table.innerHTML = "";

    if (!recommendations.length) {

        table.innerHTML = `

            <tr>

                <td colspan="3" class="text-center">

                    No recommendations available.

                </td>

            </tr>

        `;

        return;

    }

    recommendations.forEach(item => {

        table.innerHTML += `

            <tr>

                <td>${item.priority || "-"}</td>

                <td>${item.category || "-"}</td>

                <td>${item.recommendation || "-"}</td>

            </tr>

        `;

    });

}

/* ==========================================================
   Simulation History
========================================================== */

function addHistory(metrics) {

    const table =
        document.getElementById("historyTable");

    if (
        table.innerText.includes("No simulation history")
    ) {

        table.innerHTML = "";

    }

    const now = new Date();

    table.insertAdjacentHTML(

        "afterbegin",

        `

        <tr>

            <td>${metrics.run_id || "-"}</td>

            <td>${metrics.building_name || "Honeywell Office"}</td>

            <td>

                <span class="status-success">

                    Completed

                </span>

            </td>

            <td>${formatValue(metrics.execution_time)}</td>

            <td>${now.toLocaleString()}</td>

        </tr>

        `

    );

    document.getElementById("latestRun").innerText =
        now.toLocaleString();

    document.getElementById("executionTime").innerText =
        formatValue(metrics.execution_time);

}

/* ==========================================================
   Helpers
========================================================== */

function formatValue(value) {

    if (value === undefined || value === null) {

        return "--";

    }

    if (typeof value === "number") {

        return value.toFixed(2);

    }

    return value;

}