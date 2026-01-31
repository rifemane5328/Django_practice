const toggleBtn = document.getElementById("themeToggle");
const navbar = document.querySelector(".theme-nav")

toggleBtn.addEventListener("click", () => {
    const isDark = document.body.dataset.theme === 'dark';
    document.body.dataset.theme = isDark ? "light" : "dark";
    navbar.setAttribute('data-bs-theme', isDark ? "light" : "dark");
});
