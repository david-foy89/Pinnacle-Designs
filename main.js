const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.querySelector(".nav-menu");
const yearEl = document.getElementById("year");
const form = document.querySelector(".contact-form");

if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

if (navToggle && navMenu) {
  navToggle.addEventListener("click", () => {
    const open = navMenu.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(open));
    navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });

  navMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navMenu.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", "Open menu");
    });
  });
}

const backToTop = document.getElementById("back-to-top");

if (backToTop) {
  const showAfter = 400;

  const updateBackToTop = () => {
    const visible = window.scrollY > showAfter;
    backToTop.classList.toggle("is-visible", visible);
    backToTop.setAttribute("aria-hidden", String(!visible));
    backToTop.tabIndex = visible ? 0 : -1;
  };

  updateBackToTop();
  window.addEventListener("scroll", updateBackToTop, { passive: true });

  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

if (form) {
  const btn = form.querySelector('button[type="submit"]');
  const status = document.getElementById("form-status");
  const originalLabel = btn?.textContent ?? "Send Message";

  const setStatus = (message, type) => {
    if (!status) return;
    status.textContent = message;
    status.className = type ? `form-status form-status--${type}` : "form-status";
    status.hidden = !message;
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setStatus("", "");

    if (!btn) return;

    btn.disabled = true;
    btn.textContent = "Sending…";

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
      });

      let data = {};
      try {
        data = await response.json();
      } catch {
        /* non-JSON error body */
      }

      if (!response.ok || data.error) {
        throw new Error(data.error || "Could not send message.");
      }

      form.reset();
      btn.textContent = "Message sent — we'll be in touch!";
      setStatus("Thanks! We'll get back to you soon.", "success");

      setTimeout(() => {
        btn.textContent = originalLabel;
        btn.disabled = false;
        setStatus("", "");
      }, 5000);
    } catch {
      btn.textContent = originalLabel;
      btn.disabled = false;
      setStatus(
        "Something went wrong. Please try again or email hello@pinnacledesigns.com directly.",
        "error"
      );
    }
  });
}
