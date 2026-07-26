document.addEventListener("DOMContentLoaded", () => {

    loadSettings();

    document
        .getElementById("saveSettings")
        .addEventListener("click", saveSettings);

});

/* ==========================================================
   Load Settings
========================================================== */

async function loadSettings() {

    try {

        /*
            Replace this with your backend endpoint.

            Example:
            GET /api/settings
        */

        const response = await fetch("/settings");

        if (!response.ok) {

            return;

        }

        const settings = await response.json();

        setValue("organization", settings.organization);
        setValue("defaultBuilding", settings.default_building);
        setValue("timezone", settings.timezone);
        setValue("theme", settings.theme);

        setValue("llmModel", settings.llm_model);
        setValue("temperature", settings.temperature);
        setValue("timeout", settings.timeout);

        setValue("weatherDirectory", settings.weather_directory);
        setValue("outputDirectory", settings.output_directory);
        setValue("parallelRuns", settings.parallel_runs);

    }

    catch (error) {

        console.error(error);

    }

}

/* ==========================================================
   Save Settings
========================================================== */

async function saveSettings() {

    const button = document.getElementById("saveSettings");

    button.disabled = true;
    button.innerText = "Saving...";

    try {

        const payload = {

            organization: getValue("organization"),
            default_building: getValue("defaultBuilding"),
            timezone: getValue("timezone"),
            theme: getValue("theme"),

            llm_model: getValue("llmModel"),
            temperature: Number(getValue("temperature")),
            timeout: Number(getValue("timeout")),

            weather_directory: getValue("weatherDirectory"),
            output_directory: getValue("outputDirectory"),
            parallel_runs: Number(getValue("parallelRuns"))

        };

        /*
            Replace with your backend endpoint.

            Example:
            POST /api/settings
        */

        const response = await fetch("/settings", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(payload)

        });

        if (!response.ok) {

            throw new Error("Unable to save settings.");

        }

        showNotification(
            "Settings saved successfully.",
            "success"
        );

    }

    catch (error) {

        console.error(error);

        showNotification(
            "Failed to save settings.",
            "error"
        );

    }

    finally {

        button.disabled = false;
        button.innerText = "Save Settings";

    }

}

/* ==========================================================
   Helpers
========================================================== */

function getValue(id) {

    return document.getElementById(id).value;

}

function setValue(id, value) {

    if (value !== undefined &&
        value !== null) {

        document.getElementById(id).value = value;

    }

}

/* ==========================================================
   Notifications
========================================================== */

function showNotification(message, type) {

    const toast = document.createElement("div");

    toast.className = `setting-toast ${type}`;

    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 50);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 300);

    }, 2500);

}