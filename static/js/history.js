document.addEventListener("DOMContentLoaded", () => {

    document
        .getElementById("refreshHistory")
        .addEventListener("click", loadHistory);

    document
        .getElementById("searchInput")
        .addEventListener("input", filterHistory);

    document
        .getElementById("statusFilter")
        .addEventListener("change", filterHistory);

    document
        .getElementById("dateFilter")
        .addEventListener("change", filterHistory);

    loadHistory();

});

let historyData = [];

/* ==========================================================
   Load History
========================================================== */

async function loadHistory() {

    const table = document.getElementById("historyTable");

    table.innerHTML = `
        <tr>
            <td colspan="7" class="text-center">
                Loading simulation history...
            </td>
        </tr>
    `;

    try {

        /*
            Replace this endpoint with your actual API.

            Example:
            GET /history
        */

        const response = await fetch("/history");

        if (!response.ok) {

            throw new Error("Unable to load history.");

        }

        historyData = await response.json();

        renderHistory(historyData);

    }

    catch (error) {

        console.error(error);

        table.innerHTML = `
            <tr>
                <td colspan="7" class="text-center">
                    Failed to load history.
                </td>
            </tr>
        `;

    }

}

/* ==========================================================
   Render Table
========================================================== */

function renderHistory(data) {

    const table = document.getElementById("historyTable");

    table.innerHTML = "";

    document.getElementById("historyCount").innerText =
        `${data.length} Runs`;

    if (!data.length) {

        table.innerHTML = `
            <tr>
                <td colspan="7" class="text-center">
                    No simulations available.
                </td>
            </tr>
        `;

        return;

    }

    data.forEach(run => {

        table.insertAdjacentHTML("beforeend", `

            <tr>

                <td>${run.run_id || "-"}</td>

                <td>${run.simulation_name || "-"}</td>

                <td>${run.building || "-"}</td>

                <td>

                    ${statusBadge(run.status)}

                </td>

                <td>

                    ${run.execution_time || "-"}

                </td>

                <td>

                    ${run.date || "-"}

                </td>

                <td>

                    <div class="action-buttons">

                        <button
                            class="action-btn"
                            onclick="viewRun('${run.run_id}')">

                            <i class="bi bi-eye"></i>

                        </button>

                        <button
                            class="action-btn"
                            onclick="deleteRun('${run.run_id}')">

                            <i class="bi bi-trash"></i>

                        </button>

                    </div>

                </td>

            </tr>

        `);

    });

}

/* ==========================================================
   Search & Filter
========================================================== */

function filterHistory() {

    const search =
        document
            .getElementById("searchInput")
            .value
            .toLowerCase();

    const status =
        document
            .getElementById("statusFilter")
            .value;

    const date =
        document
            .getElementById("dateFilter")
            .value;

    const filtered = historyData.filter(run => {

        const matchesSearch =

            (run.run_id || "")
                .toLowerCase()
                .includes(search)

            ||

            (run.building || "")
                .toLowerCase()
                .includes(search)

            ||

            (run.simulation_name || "")
                .toLowerCase()
                .includes(search);

        const matchesStatus =

            !status ||

            run.status === status;

        const matchesDate =

            !date ||

            (run.date || "")
                .startsWith(date);

        return (

            matchesSearch &&
            matchesStatus &&
            matchesDate

        );

    });

    renderHistory(filtered);

}

/* ==========================================================
   View Details
========================================================== */

function viewRun(runId) {

    const run = historyData.find(item => item.run_id == runId);

    if (!run) {

        return;

    }

    document.getElementById("analysisPanel").innerText =

        run.analysis ||

        "No AI analysis available.";

    const recommendationPanel =
        document.getElementById("recommendationPanel");

    recommendationPanel.innerHTML = "";

    if (!run.recommendations ||
        !run.recommendations.length) {

        recommendationPanel.innerText =
            "No recommendations available.";

        return;

    }

    const ul = document.createElement("ul");

    run.recommendations.forEach(item => {

        const li = document.createElement("li");

        li.innerText =

            typeof item === "string"

            ? item

            : item.recommendation ||
              item.message ||
              JSON.stringify(item);

        ul.appendChild(li);

    });

    recommendationPanel.appendChild(ul);

}

/* ==========================================================
   Delete
========================================================== */

async function deleteRun(runId) {

    if (!confirm("Delete this simulation run?")) {

        return;

    }

    try {

        /*
            Replace with your API

            DELETE /history/<id>
        */

        const response = await fetch(

            `/history/${runId}`,

            {

                method: "DELETE"

            }

        );

        if (!response.ok) {

            throw new Error();

        }

        historyData = historyData.filter(

            run => run.run_id != runId

        );

        renderHistory(historyData);

        document.getElementById("analysisPanel").innerText =
            "Select a simulation to view its AI analysis.";

        document.getElementById("recommendationPanel").innerText =
            "Recommendations will appear here.";

    }

    catch {

        alert("Unable to delete simulation.");

    }

}

/* ==========================================================
   Status Badge
========================================================== */

function statusBadge(status) {

    switch ((status || "").toLowerCase()) {

        case "completed":

            return `<span class="status-success">Completed</span>`;

        case "running":

            return `<span class="status-running">Running</span>`;

        case "failed":

            return `<span class="status-failed">Failed</span>`;

        default:

            return status || "-";

    }

}