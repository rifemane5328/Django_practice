document.addEventListener("DOMContentLoaded", () => {

    // smooth page rendering
    document.body.classList.add("fade-in");
    setTimeout(() => {
        document.body.classList.add("show");
    }, 100);

    // backlight when changing material's quantity +/-
    document.querySelectorAll("a[href*='inc'], a[href*='dec']").forEach(btn => { // all <a> with href="inc" or "dec"
        btn.addEventListener("click", () => {
            const row = btn.closest("tr");
            if (!row) return;

            row.classList.add("table-info");
            setTimeout(() => {
                row.classList.remove("table-info");
            }, 600);

        });
    });

    const observer = new IntersectionObserver(entries => { // when an entry appears in user's view
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            } else {
                entry.target.classList.remove("show");
            }
        });
    });
    document.querySelectorAll(".fade-in").forEach(el => observer.observe(el));
});                    