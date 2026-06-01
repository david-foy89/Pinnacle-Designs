const FORMSPREE_ENDPOINT = "https://formspree.io/f/xojbzjog";

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

function formatFormspreeError(data) {
  if (data?.errors?.length) {
    return data.errors.map((e) => e.message).join(" ");
  }
  if (typeof data?.error === "string") {
    return data.error;
  }
  return "Could not send message. Please try again.";
}

async function submitToFormspree(formEl) {
  const response = await fetch(FORMSPREE_ENDPOINT, {
    method: "POST",
    body: new FormData(formEl),
    headers: { Accept: "application/json" },
  });

  let data = {};
  try {
    data = await response.json();
  } catch {
    if (response.ok) {
      return { ok: true };
    }
  }

  if (response.ok && data.ok) {
    return { ok: true };
  }

  return { ok: false, message: formatFormspreeError(data) };
}

if (form) {
  form.setAttribute("action", FORMSPREE_ENDPOINT);
  form.setAttribute("method", "POST");

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

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    setStatus("", "");

    if (btn) {
      btn.disabled = true;
      btn.textContent = "Sending…";
    }

    try {
      const result = await submitToFormspree(form);

      if (result.ok) {
        form.reset();
        if (btn) btn.textContent = "Message sent — we'll be in touch!";
        setStatus("Thanks! We'll get back to you soon.", "success");

        setTimeout(() => {
          if (btn) {
            btn.textContent = originalLabel;
            btn.disabled = false;
          }
          setStatus("", "");
        }, 5000);
        return;
      }

      setStatus(result.message, "error");
      if (btn) {
        btn.textContent = originalLabel;
        btn.disabled = false;
      }
    } catch {
      setStatus("Submitting via backup…", "success");
      if (btn) {
        btn.textContent = originalLabel;
        btn.disabled = false;
      }
      HTMLFormElement.prototype.submit.call(form);
    }
  });
}
