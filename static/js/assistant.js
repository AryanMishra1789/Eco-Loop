document.addEventListener("DOMContentLoaded", () => {

    const sendButton = document.getElementById("sendMessage");
    const input = document.getElementById("chatInput");

    sendButton.addEventListener("click", sendMessage);

    input.addEventListener("keydown", function (event) {

        if (event.key === "Enter" && !event.shiftKey) {

            event.preventDefault();

            sendMessage();

        }

    });

    document.querySelectorAll(".prompt-btn").forEach(button => {

        button.addEventListener("click", function () {

            input.value = this.innerText.trim();

            sendMessage();

        });

    });

});

/* ==========================================================
   Send Message
========================================================== */

async function sendMessage() {

    const input = document.getElementById("chatInput");
    const sendButton = document.getElementById("sendMessage");
    const toolOutput = document.getElementById("toolOutput");

    const message = input.value.trim();

    if (!message) {
        return;
    }

    appendUserMessage(message);

    input.value = "";

    sendButton.disabled = true;
    sendButton.innerText = "Processing...";

    toolOutput.textContent =
`Processing request...

✓ Understanding prompt
✓ Selecting workflow
✓ Running EnergyPlus simulation
✓ Generating AI recommendations

Please wait...`;

    const loading = appendLoadingMessage();

    try {

        const response = await fetch("/api/agent/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                message: message

            })

        });

        if (!response.ok) {

            throw new Error("Request failed.");

        }

        const result = await response.json();

        removeLoadingMessage(loading);

        appendAIMessage(getAssistantResponse(result));

        updateToolOutput(result);

    }

    catch (error) {

        removeLoadingMessage(loading);

        appendAIMessage(
            "Sorry, something went wrong while processing your request."
        );

        toolOutput.textContent =
            "Error\n\n" + error.message;

        console.error(error);

    }

    finally {

        sendButton.disabled = false;
        sendButton.innerText = "Send";

    }

}

/* ==========================================================
   Chat Messages
========================================================== */

function appendUserMessage(message) {

    appendMessage("user", "You", message);

}

function appendAIMessage(message) {

    appendMessage("ai", "AI", message);

}

function appendMessage(type, avatar, message) {

    const container = document.getElementById("chatMessages");

    const html = `

        <div class="message ${type}">

            <div class="message-avatar">

                ${avatar}

            </div>

            <div class="message-content">

                ${escapeHtml(message)}

            </div>

        </div>

    `;

    container.insertAdjacentHTML("beforeend", html);

    scrollChatToBottom();

}

/* ==========================================================
   Loading Bubble
========================================================== */

function appendLoadingMessage() {

    const container = document.getElementById("chatMessages");

    const wrapper = document.createElement("div");

    wrapper.className = "message ai";

    wrapper.id = "loadingMessage";

    wrapper.innerHTML = `

        <div class="message-avatar">

            AI

        </div>

        <div class="message-content">

            Running EnergyPlus simulation...
            <br><br>
            Please wait.

        </div>

    `;

    container.appendChild(wrapper);

    scrollChatToBottom();

    return wrapper;

}

function removeLoadingMessage(element) {

    if (element) {

        element.remove();

    }

}

/* ==========================================================
   Assistant Response
========================================================== */

function getAssistantResponse(response) {

    if (response.response) {

        return response.response;

    }

    if (
        response.tool_result &&
        response.tool_result.result &&
        response.tool_result.result.analysis
    ) {

        return response.tool_result.result.analysis;

    }

    if (response.message) {

        return response.message;

    }

    return JSON.stringify(response, null, 2);

}

/* ==========================================================
   Tool Execution
========================================================== */

function updateToolOutput(response) {

    const output = document.getElementById("toolOutput");

    let text = "";

    text += "Intent\n";
    text += "------\n";
    text += (response.intent || "Unknown") + "\n\n";

    text += "Workflow\n";
    text += "--------\n";
    text += (response.workflow || "Unknown") + "\n\n";

    if (response.tool_result) {

        text += "Execution Status\n";
        text += "----------------\n";
        text += (response.tool_result.success ? "Success" : "Failed") + "\n\n";

        if (response.tool_result.execution_time_ms) {

            text += "Execution Time\n";
            text += "--------------\n";
            text += response.tool_result.execution_time_ms.toFixed(2) + " ms\n\n";

        }

        if (response.tool_result.service) {

            text += "Service\n";
            text += "-------\n";
            text += response.tool_result.service + "\n\n";

        }

        if (response.tool_result.result) {

            const result = response.tool_result.result;

            if (result.metrics) {

                text += "Simulation Metrics\n";
                text += "------------------\n";

                Object.entries(result.metrics).forEach(([key, value]) => {

                    text += `${key}: ${value}\n`;

                });

                text += "\n";

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

                text += "\n";

            }

        }

    }

    output.textContent = text;

}

/* ==========================================================
   Utilities
========================================================== */

function scrollChatToBottom() {

    const container = document.getElementById("chatMessages");

    container.scrollTop = container.scrollHeight;

}

function escapeHtml(text) {

    const div = document.createElement("div");

    div.innerText = text;

    return div.innerHTML;

}