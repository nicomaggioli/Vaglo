/* VAGLO marketing site. No dependencies. Set contactEmail to enable mail drafts. */
(() => {
  "use strict";
  const config = { contactEmail: "" };
  const header = document.querySelector(".site-header");
  const updateHeader = () =>
    header?.classList.toggle("scrolled", window.scrollY > 10);
  window.addEventListener("scroll", updateHeader, { passive: true });
  updateHeader();
  const menuButton = document.querySelector(".menu-toggle");
  const menu = document.querySelector("#mobile-menu");
  function closeMenu() {
    if (!menuButton) return;
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Open menu");
    menu.hidden = true;
  }
  menuButton?.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") !== "true";
    menu.hidden = !open;
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });
  menu
    ?.querySelectorAll("a")
    .forEach((a) => a.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !menu.hidden) {
      closeMenu();
      menuButton.focus();
    }
  });
  window.matchMedia("(min-width: 581px)").addEventListener("change", (e) => {
    if (e.matches) closeMenu();
  });

  const tabs = [...document.querySelectorAll("[data-product]")];
  function selectTab(tab, focus = false) {
    tabs.forEach((t) => {
      const selected = t === tab;
      t.setAttribute("aria-selected", String(selected));
      t.tabIndex = selected ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden =
        !selected;
    });
    if (focus) tab.focus();
  }
  tabs.forEach((tab, i) => {
    tab.addEventListener("click", () => selectTab(tab));
    tab.addEventListener("keydown", (e) => {
      let next = i;
      if (e.key === "ArrowRight") next = (i + 1) % tabs.length;
      else if (e.key === "ArrowLeft")
        next = (i + tabs.length - 1) % tabs.length;
      else if (e.key === "Home") next = 0;
      else if (e.key === "End") next = tabs.length - 1;
      else return;
      e.preventDefault();
      selectTab(tabs[next], true);
    });
  });

  const dialog = document.querySelector("#trailer-dialog");
  const video = document.querySelector("#full-video");
  const preview = document.querySelector("#hero-video");
  const previewToggle = document.querySelector("#preview-toggle");
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  let lastFocus = null,
    previewRequested = false;
  function previewLabel() {
    if (!previewToggle) return;
    previewToggle.setAttribute(
      "aria-label",
      preview.paused ? "Play background preview" : "Pause background preview",
    );
    previewToggle.textContent = preview.paused ? "▶" : "Ⅱ";
  }
  function playPreview() {
    if (!preview.src) {
      preview.src = "assets/hero-loop.mp4";
      preview.load();
    }
    preview
      .play()
      .catch(() => {})
      .finally(previewLabel);
  }
  if (preview) {
    preview.addEventListener("play", previewLabel);
    preview.addEventListener("pause", previewLabel);
    previewToggle.addEventListener("click", () => {
      previewRequested = preview.paused;
      if (previewRequested) playPreview();
      else preview.pause();
    });
    // Static poster by default: visitors choose when the film starts.
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) preview.pause();
      else if (previewRequested && !dialog.open) playPreview();
    });
    if ("IntersectionObserver" in window)
      new IntersectionObserver(
        (entries) => {
          if (!entries[0].isIntersecting) preview.pause();
          else if (previewRequested && !dialog.open && !document.hidden)
            playPreview();
        },
        { threshold: 0.1 },
      ).observe(preview);
    reducedMotion.addEventListener("change", (e) => {
      if (e.matches) {
        previewRequested = false;
        preview.pause();
      }
    });
  }
  function closeTrailer() {
    dialog.close();
  }
  if (dialog) {
    document.querySelectorAll("[data-trailer]").forEach((button) =>
      button.addEventListener("click", () => {
        lastFocus = button;
        preview.pause();
        dialog.showModal();
        document.body.classList.add("modal-open");
        video.play().catch(() => {
          /* Native controls remain available if autoplay is blocked. */
        });
      }),
    );
    dialog
      .querySelector(".dialog-close")
      .addEventListener("click", closeTrailer);
    dialog.addEventListener("click", (e) => {
      const r = dialog.getBoundingClientRect();
      if (
        e.target === dialog &&
        (e.clientX < r.left ||
          e.clientX > r.right ||
          e.clientY < r.top ||
          e.clientY > r.bottom)
      )
        closeTrailer();
    });
    dialog.addEventListener("close", () => {
      video.pause();
      document.body.classList.remove("modal-open");
      lastFocus?.focus();
      if (previewRequested && !document.hidden) playPreview();
    });
    dialog.querySelectorAll("[data-time]").forEach((button) =>
      button.addEventListener("click", () => {
        const seek = () => {
          video.currentTime = Number(button.dataset.time);
          video.play().catch(() => {});
        };
        if (video.readyState >= 1) seek();
        else {
          video.addEventListener("loadedmetadata", seek, { once: true });
          video.load();
        }
      }),
    );
  }

  const form = document.querySelector("#callform");
  if (form) {
    const result = document.querySelector("#form-result");
    const request = document.querySelector("#request-text");
    const validEmail =
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(config.contactEmail) &&
      !config.contactEmail.endsWith(".example");
    if (validEmail)
      document.querySelector("#delivery-note").textContent =
        "We’ll prepare an email in your mail app. Review it and send when you’re ready.";
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const d = new FormData(form);
      const text = `VAGLO demo request\n\nName: ${d.get("name")}\nEmail: ${d.get("email")}\nFirm: ${d.get("firm")}\nTeam size: ${d.get("team_size") || "Not specified"}\nDiscipline: ${d.get("discipline") || "Not specified"}\n\nCurrent challenge:\n${d.get("workflow")}`;
      request.value = text;
      result.hidden = false;
      if (validEmail) {
        const a = document.createElement("a");
        a.href = `mailto:${config.contactEmail}?subject=${encodeURIComponent("VAGLO demo — " + d.get("firm"))}&body=${encodeURIComponent(text)}`;
        a.click();
        document.querySelector("#result-message").textContent =
          "Your mail app should open with a draft. Review and send it there. If it does not open, copy or save the request below.";
      }
      result.scrollIntoView({
        behavior: reducedMotion.matches ? "auto" : "smooth",
        block: "nearest",
      });
    });
    const copy = document.querySelector("#copy-request");
    copy.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(request.value);
        copy.textContent = "Copied";
        setTimeout(() => (copy.textContent = "Copy request"), 2500);
      } catch {
        request.focus();
        request.select();
        copy.textContent = "Select and copy the text";
      }
    });
    document.querySelector("#save-request").addEventListener("click", () => {
      const url = URL.createObjectURL(
        new Blob([request.value], { type: "text/plain;charset=utf-8" }),
      );
      const link = document.createElement("a");
      link.href = url;
      link.download = "vaglo-demo-request.txt";
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
  }
})();
