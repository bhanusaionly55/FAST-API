// 🔹 Page load animation
window.addEventListener("load", () => {
    document.body.classList.add("loaded");
});

// 🔹 Smooth redirect
function smoothRedirect(page) {
    document.body.style.opacity = "0";
    setTimeout(() => {
        window.location.href = page;
    }, 400);
}

// 🔐 LOGIN
function login() {
    let user = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username: user, password: password })
    })
    .then(res => {
        if (!res.ok) throw new Error("Invalid credentials");
        return res.json();
    })
    .then(data => {
        localStorage.setItem("user_id", data.id);
        smoothRedirect("journal.html");
    })
    .catch(() => alert("Incorrect username or password"));
}

// 🆕 REGISTER
function register() {
    let user = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username: user, password: password })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw new Error(err.detail); });
        }
        return res.json();
    })
    .then(() => {
        alert("User registered successfully");
        smoothRedirect("index.html");
    })
    .catch(err => alert(err.message));
}

// 🔄 NAVIGATION
function goToRegister() {
    smoothRedirect("new.html");
}

// 📖 LOAD JOURNAL
window.onload = function () {
    let user_id = localStorage.getItem("user_id");

    if (!user_id) return;

    fetch(`http://127.0.0.1:8000/journal/${user_id}`)
        .then(res => res.json())
        .then(data => {
            let area = document.getElementById("journal");
            if (area) area.value = data.content;
        });
};

// 💾 SAVE JOURNAL
function saveJournal() {
    let user_id = localStorage.getItem("user_id");
    let content = document.getElementById("journal").value;

    fetch(`http://127.0.0.1:8000/journal/${user_id}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ content: content })
    })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(() => alert("Saved successfully"))
    .catch(() => alert("Error saving journal"));
}

// ✍️ Auto-grow textarea
document.addEventListener("input", (e) => {
    if (e.target.id === "journal") {
        e.target.style.height = "auto";
        e.target.style.height = e.target.scrollHeight + "px";
    }
});

function deleteUser() {
    let confirmDelete = confirm("Are you sure you want to permanently delete your records?");

    if (!confirmDelete) return;

    let user_id = localStorage.getItem("user_id");

    fetch(`http://127.0.0.1:8000/user/${user_id}`, {
        method: "DELETE"
    })
    .then(res => {
        if (!res.ok) throw new Error("Delete failed");
        return res.json();
    })
    .then(() => {
        alert("Account deleted");

        // clear storage
        localStorage.removeItem("user_id");

        // redirect to login
        window.location.href = "index.html";
    })
    .catch(() => {
        alert("Error deleting account");
    });
}