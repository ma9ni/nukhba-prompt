(function initOptions() {
  const constants = NukhbaPromptConstants;
  const storage = NukhbaPromptStorage;

  const form = document.getElementById("settings-form");
  const status = document.getElementById("status");
  const resetButton = document.getElementById("reset-defaults");

  const fields = {
    openrouterApiKey: document.getElementById("openrouterApiKey"),
    openrouterModel: document.getElementById("openrouterModel"),
    buttonLabel: document.getElementById("buttonLabel"),
    systemPrompt: document.getElementById("systemPrompt")
  };

  hydrate();

  form.addEventListener("submit", async function handleSubmit(event) {
    event.preventDefault();

    const payload = {
      openrouterApiKey: fields.openrouterApiKey.value.trim(),
      openrouterModel: fields.openrouterModel.value.trim(),
      buttonLabel: fields.buttonLabel.value.trim() || constants.DEFAULTS.buttonLabel,
      systemPrompt: fields.systemPrompt.value.trim()
    };

    if (!payload.openrouterApiKey || !payload.openrouterModel || !payload.systemPrompt) {
      renderStatus("All required fields must be filled.", "error");
      return;
    }

    try {
      await storage.saveSettings(payload);
      renderStatus("Settings saved.", "success");
    } catch (error) {
      renderStatus(error.message || "Unable to save settings.", "error");
    }
  });

  resetButton.addEventListener("click", async function handleReset() {
    try {
      await storage.saveSettings(constants.DEFAULTS);
      applyValues(constants.DEFAULTS);
      renderStatus("Defaults restored.", "success");
    } catch (error) {
      renderStatus(error.message || "Unable to restore defaults.", "error");
    }
  });

  async function hydrate() {
    try {
      const settings = await storage.getSettings();
      applyValues(settings);
    } catch (error) {
      renderStatus(error.message || "Unable to load settings.", "error");
    }
  }

  function applyValues(values) {
    fields.openrouterApiKey.value = values.openrouterApiKey || "";
    fields.openrouterModel.value = values.openrouterModel || "";
    fields.buttonLabel.value = values.buttonLabel || constants.DEFAULTS.buttonLabel;
    fields.systemPrompt.value = values.systemPrompt || constants.DEFAULTS.systemPrompt;
  }

  function renderStatus(message, state) {
    status.textContent = message;
    status.dataset.state = state;
  }
})();
