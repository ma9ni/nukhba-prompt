(function initContentScript() {
  const constants = NukhbaPromptConstants;
  const dom = NukhbaPromptDom;

  const state = {
    activeField: null,
    buttonLabel: constants.DEFAULTS.buttonLabel,
    isLoading: false,
    isShowingError: false
  };

  const root = document.createElement("div");
  root.id = constants.UI.ROOT_ID;
  root.innerHTML = [
    '<button id="' + constants.UI.BUTTON_ID + '" type="button" class="nukhba-prompt-button">',
    constants.DEFAULTS.buttonLabel,
    "</button>",
    '<div class="nukhba-prompt-status" aria-live="polite"></div>'
  ].join("");
  document.documentElement.appendChild(root);

  const button = root.querySelector("#" + constants.UI.BUTTON_ID);
  const status = root.querySelector(".nukhba-prompt-status");

  loadButtonLabel();
  attachListeners();
  scanAndAttach();
  updateButtonVisibility();

  function attachListeners() {
    document.addEventListener("focusin", handleFocusChange, true);
    document.addEventListener("pointerdown", handlePointerEvent, true);
    window.addEventListener("scroll", updateButtonPosition, true);
    window.addEventListener("resize", updateButtonPosition);
    button.addEventListener("click", handleOptimizeClick);

    const observer = new MutationObserver(function onMutation() {
      scanAndAttach();
      updateButtonVisibility();
    });

    observer.observe(document.body || document.documentElement, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["class", "style", "contenteditable", "role"]
    });
  }

  function loadButtonLabel() {
    chrome.storage.local.get(
      { buttonLabel: constants.DEFAULTS.buttonLabel },
      function applyLabel(items) {
        state.buttonLabel = items.buttonLabel || constants.DEFAULTS.buttonLabel;
        renderIdleState();
      }
    );

    chrome.storage.onChanged.addListener(function onStorageChange(changes, areaName) {
      if (areaName !== "local" || !changes.buttonLabel) {
        return;
      }
      state.buttonLabel = changes.buttonLabel.newValue || constants.DEFAULTS.buttonLabel;
      if (!state.isLoading && !state.isShowingError) {
        renderIdleState();
      }
    });
  }

  function scanAndAttach() {
    const fields = dom.findPromptFields();
    if (!state.activeField || !dom.isSupportedPromptField(state.activeField)) {
      state.activeField = fields[0] || null;
    }
  }

  function handleFocusChange(event) {
    const target = event.target;
    if (dom.isSupportedPromptField(target)) {
      state.activeField = target;
      updateButtonVisibility();
    }
  }

  function handlePointerEvent(event) {
    const targetField = event.target && event.target.closest
      ? event.target.closest("textarea, [contenteditable='true'], [contenteditable='plaintext-only'], [role='textbox']")
      : null;

    if (dom.isSupportedPromptField(targetField)) {
      state.activeField = targetField;
      updateButtonVisibility();
    }
  }

  function updateButtonVisibility() {
    const field = state.activeField;
    if (!dom.isSupportedPromptField(field)) {
      root.classList.remove("is-visible");
      return;
    }

    root.classList.add("is-visible");
    updateButtonPosition();
  }

  function updateButtonPosition() {
    const field = state.activeField;
    if (!dom.isSupportedPromptField(field)) {
      root.classList.remove("is-visible");
      return;
    }

    const rect = field.getBoundingClientRect();
    const offsetX = Math.min(12, rect.width * 0.08);
    const offsetY = Math.min(12, rect.height * 0.18);

    root.style.top = Math.max(8, rect.bottom - offsetY - button.offsetHeight) + "px";
    root.style.left = Math.max(8, rect.right - offsetX - button.offsetWidth) + "px";
  }

  async function handleOptimizeClick() {
    const field = state.activeField;
    if (!dom.isSupportedPromptField(field) || state.isLoading) {
      return;
    }

    const promptText = dom.getPromptValue(field);
    if (!promptText) {
      showStatus("No prompt found.");
      return;
    }

    state.isLoading = true;
    button.disabled = true;
    button.textContent = "Optimizing...";
    status.textContent = "";
    status.dataset.state = "";
    updateButtonPosition();

    try {
      const response = await chrome.runtime.sendMessage({
        type: constants.MESSAGE_TYPES.OPTIMIZE_PROMPT,
        prompt: promptText,
        site: dom.detectSite()
      });

      if (!response || !response.ok) {
        throw new Error((response && response.error) || "Optimization failed.");
      }

      dom.setPromptValue(field, response.optimizedPrompt);
      renderIdleState();
    } catch (error) {
      showStatus(error.message || "Network error.");
    } finally {
      state.isLoading = false;
      button.disabled = false;
      if (!state.isShowingError) {
        renderIdleState();
      }
      updateButtonPosition();
    }
  }

  function renderIdleState() {
    state.isShowingError = false;
    button.textContent = state.buttonLabel;
    status.textContent = "";
    status.dataset.state = "";
  }

  function showStatus(message) {
    state.isShowingError = true;
    button.textContent = state.buttonLabel;
    status.textContent = message;
    status.dataset.state = "error";

    window.clearTimeout(showStatus.timeoutId);
    showStatus.timeoutId = window.setTimeout(function clearStatus() {
      state.isShowingError = false;
      status.textContent = "";
      status.dataset.state = "";
    }, constants.UI.ERROR_TIMEOUT_MS);
  }
})();
