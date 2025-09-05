// Cookie helpers
function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + (days*24*60*60*1000));
    document.cookie = name + "=" + encodeURIComponent(value) + ";expires=" + d.toUTCString() + ";path=/";
}

function getCookie(name) {
    const cookies = document.cookie.split(";").map(c => c.trim());
    for (let c of cookies) {
        if (c.startsWith(name + "=")) return decodeURIComponent(c.substring(name.length + 1));
    }
    return null;
}

// Toggle dark mode override
function toggleDarkMode() {
    const html = document.documentElement;
    if(html.getAttribute("data-theme") === "light") {
        html.removeAttribute("data-theme");
        setCookie("darkModeDisabled", "false", 30);
    } else {
        html.setAttribute("data-theme", "light");
        setCookie("darkModeDisabled", "true", 30);
    }
}

// Apply saved preference on load
window.addEventListener("DOMContentLoaded", () => {
    if(getCookie("darkModeDisabled") === "true") {
        document.documentElement.setAttribute("data-theme", "light");
    }

    const btn = document.getElementById("theme-toggle");
    if(btn) btn.addEventListener("click", toggleDarkMode);
});
