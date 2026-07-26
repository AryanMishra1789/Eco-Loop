document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");
    const demoButton = document.getElementById("demoButton");

    loadRememberedUser();

    loginForm.addEventListener("submit", login);

    demoButton.addEventListener("click", demoLogin);

});

/* ==========================================================
   Login
========================================================== */

async function login(event) {

    event.preventDefault();

    clearError();

    const email = getValue("email").trim();
    const password = getValue("password");
    const remember = document.getElementById("rememberMe").checked;

    if (!validate(email, password)) {

        return;

    }

    const button = document.getElementById("loginButton");

    setLoading(button, true);

    try {

        const response = await fetch("/login", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email,
                password

            })

        });

        const result = await response.json();

        if (!response.ok) {

            throw new Error(

                result.message || "Invalid credentials."

            );

        }

        if (remember) {

            localStorage.setItem(

                "ecoloop_email",

                email

            );

        }

        else {

            localStorage.removeItem(

                "ecoloop_email"

            );

        }

        window.location.href = "/dashboard";

    }

    catch (error) {

        showError(error.message);

    }

    finally {

        setLoading(button, false);

    }

}

/* ==========================================================
   Demo Login
========================================================== */

function demoLogin() {

    setValue("email", "demo@ecoloop.ai");

    setValue("password", "demo123");

    document.getElementById("rememberMe").checked = true;

    document
        .getElementById("loginForm")
        .requestSubmit();

}

/* ==========================================================
   Validation
========================================================== */

function validate(email, password) {

    if (!email) {

        showError("Email is required.");

        return false;

    }

    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!regex.test(email)) {

        showError("Enter a valid email address.");

        return false;

    }

    if (!password) {

        showError("Password is required.");

        return false;

    }

    if (password.length < 6) {

        showError(

            "Password must contain at least 6 characters."

        );

        return false;

    }

    return true;

}

/* ==========================================================
   Remember Me
========================================================== */

function loadRememberedUser() {

    const savedEmail = localStorage.getItem(

        "ecoloop_email"

    );

    if (savedEmail) {

        setValue("email", savedEmail);

        document.getElementById(

            "rememberMe"

        ).checked = true;

    }

}

/* ==========================================================
   Helpers
========================================================== */

function getValue(id) {

    return document.getElementById(id).value;

}

function setValue(id, value) {

    document.getElementById(id).value = value;

}

function setLoading(button, loading) {

    if (loading) {

        button.disabled = true;

        button.innerHTML = `

            <span
                class="spinner-border spinner-border-sm me-2">
            </span>

            Signing In...

        `;

    }

    else {

        button.disabled = false;

        button.innerHTML = `

            <i class="bi bi-box-arrow-in-right me-2"></i>

            Sign In

        `;

    }

}

/* ==========================================================
   Error Handling
========================================================== */

function showError(message) {

    const alert = document.getElementById(

        "loginError"

    );

    alert.textContent = message;

    alert.classList.remove("d-none");

}

function clearError() {

    const alert = document.getElementById(

        "loginError"

    );

    alert.textContent = "";

    alert.classList.add("d-none");

}