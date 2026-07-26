document.addEventListener("DOMContentLoaded", () => {

    document
        .getElementById("startSimulation")
        .addEventListener("click", startSimulation);

});

/* ==========================================================
   Start Simulation
========================================================== */

async function startSimulation() {

    const button = document.getElementById("startSimulation");
    const status = document.getElementById("simulationStatus");
    const output = document.getElementById("simulationOutput");

    button.disabled = true;
    button.classList.add("btn-loading");
    button.innerText = "Running...";

    status.className = "status-running";
    status.innerText = "Running EnergyPlus simulation...";

    output.textContent =
`Initializing EcoLoop AI...

✓ Reading building configuration
✓ Preparing simulation
✓ Running EnergyPlus
✓ Generating AI recommendations

Please wait...`;

    try {

        const prompt = buildSimulationPrompt();

        const response = await fetch("/api/agent/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                message: prompt

            })

        });

        if (!response.ok) {

            throw new Error("Failed to run simulation.");

        }

        const data = await response.json();

        displayResults(data);

        status.className = "status-success";
        status.innerText = "Simulation completed successfully.";

    }

    catch (error) {

        console.error(error);

        status.className = "status-error";
        status.innerText = "Simulation failed.";

        output.textContent =
            "Error\n\n" + error.message;

    }

    finally {

        button.disabled = false;
        button.classList.remove("btn-loading");
        button.innerText = "Start Simulation";

    }

}

/* ==========================================================
   Build Prompt
========================================================== */

function buildSimulationPrompt() {

    const building =
        document.getElementById("buildingName").value;

    const simulation =
        document.getElementById("simulationName").value;

    const weather =
        document.getElementById("weatherFile").value;

    const period =
        document.getElementById("simulationPeriod").value;

    const occupancy =
        document.getElementById("occupancy").value;

    const area =
        document.getElementById("floorArea").value;

    const floors =
        document.getElementById("floors").value;

    const cooling =
        document.getElementById("coolingSetpoint").value;

    const heating =
        document.getElementById("heatingSetpoint").value;

    const ventilation =
        document.getElementById("ventilation").value;

    return `
Run an EnergyPlus simulation.

Building Name: ${building}
Simulation Name: ${simulation}
Weather File: ${weather}
Simulation Period: ${period}

Building Parameters
- Occupancy: ${occupancy}
- Floor Area: ${area}
- Floors: ${floors}

HVAC Parameters
- Cooling Setpoint: ${cooling}
- Heating Setpoint: ${heating}
- Ventilation Rate: ${ventilation}

After the simulation,
analyze the results and generate optimization recommendations.
`;

}

/* ==========================================================
   Display Results
========================================================== */

function displayResults(response) {

    const output =
        document.getElementById("simulationOutput");

    let text = "";

    text += "Intent\n";
    text += "------\n";
    text += (response.intent || "-") + "\n\n";

    text += "Workflow\n";
    text += "--------\n";
    text += (response.workflow || "-") + "\n\n";

    if (!response.tool_result) {

        output.textContent = text;

        return;

    }

    text += "Execution Status\n";
    text += "----------------\n";
    text += (response.tool_result.success ? "Success" : "Failed") + "\n\n";

    text += "Service\n";
    text += "-------\n";
    text += (response.tool_result.service || "-") + "\n\n";

    if (response.tool_result.execution_time_ms) {

        text += "Execution Time\n";
        text += "--------------\n";
        text += response.tool_result.execution_time_ms.toFixed(2) + " ms\n\n";

    }

    const result = response.tool_result.result;

    if (result.metrics) {

        text += "Simulation Metrics\n";
        text += "------------------\n";

        Object.entries(result.metrics).forEach(([key, value]) => {

            text += `${key}: ${value}\n`;

        });

        text += "\n";

    }

    if (result.analysis) {

        text += "AI Analysis\n";
        text += "-----------\n";

        text += result.analysis + "\n\n";

    }

    if (
        result.recommendations &&
        result.recommendations.length
    ) {

        text += "Recommendations\n";
        text += "---------------\n";

        result.recommendations.forEach((item, index) => {

            text += `${index + 1}. ${item.recommendation}\n`;

        });

    }

    output.textContent = text;

}