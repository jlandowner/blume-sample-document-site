(() => {
  const copiedText = () => document.body?.dataset.i18nCopied || "Copied!";
  const copyText = async (text) => {
    if (!text) return false;

    if (navigator.clipboard?.writeText && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch {
        // Fall through to the legacy path for browsers that expose but reject it.
      }
    }

    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.top = "0";
    textarea.style.left = "0";
    textarea.style.width = "1px";
    textarea.style.height = "1px";
    textarea.style.opacity = "0";
    textarea.style.pointerEvents = "none";
    document.body.append(textarea);
    textarea.focus();
    textarea.select();
    textarea.setSelectionRange(0, textarea.value.length);

    try {
      return document.execCommand("copy");
    } finally {
      textarea.remove();
    }
  };

  const liveRegion = () => {
    let region = document.querySelector("[data-docs-copy-live]");
    if (!region) {
      region = document.createElement("span");
      region.dataset.docsCopyLive = "";
      region.className = "sr-only";
      region.setAttribute("aria-live", "polite");
      document.body.append(region);
    }
    return region;
  };

  const setCopiedState = (button) => {
    const previousLabel = button.getAttribute("aria-label") || "";
    const icons = button.querySelectorAll("svg");
    button.setAttribute("aria-label", copiedText());
    icons[0]?.classList.remove("scale-0");
    icons[1]?.classList.add("scale-0");
    liveRegion().textContent = copiedText();

    window.setTimeout(() => {
      if (previousLabel) button.setAttribute("aria-label", previousLabel);
      icons[0]?.classList.add("scale-0");
      icons[1]?.classList.remove("scale-0");
      liveRegion().textContent = "";
    }, 1500);
  };

  const codeTextFor = (button) => {
    const code = button.closest("pre")?.querySelector("code");
    if (!code) return "";

    const clone = code.cloneNode(true);
    clone.querySelectorAll(".twoslash-popup-container").forEach((node) => node.remove());
    return clone.textContent || "";
  };

  document.addEventListener(
    "click",
    (event) => {
      const target = event.target;
      if (!(target instanceof Element)) return;

      const button = target.closest("[data-blume-copy]");
      if (!(button instanceof HTMLButtonElement)) return;

      event.preventDefault();
      event.stopImmediatePropagation();

      void copyText(codeTextFor(button)).then((ok) => {
        if (ok) setCopiedState(button);
      });
    },
    true,
  );
})();
