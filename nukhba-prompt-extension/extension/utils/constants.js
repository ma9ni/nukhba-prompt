(function initConstants(global) {
  const DEFAULT_SYSTEM_PROMPT = [
    "You are an expert prompt engineer.",
    "",
    "Your job is to rewrite the user's prompt so it becomes clearer, more precise, and more effective for AI systems such as ChatGPT or Claude.",
    "",
    "Rules:",
    "- Preserve the original intent",
    "- Do not answer the user's request",
    "- Do not add explanations",
    "- Do not wrap the result in quotes",
    "- Return only the improved prompt text",
    "- Make the prompt more structured, specific, and actionable",
    "- If the original prompt is already good, improve it slightly without overcomplicating it"
  ].join("\n");

  global.NukhbaPromptConstants = {
    STORAGE_KEYS: {
      OPENROUTER_API_KEY: "openrouterApiKey",
      OPENROUTER_MODEL: "openrouterModel",
      SYSTEM_PROMPT: "systemPrompt",
      BUTTON_LABEL: "buttonLabel"
    },
    DEFAULTS: {
      openrouterApiKey: "",
      openrouterModel: "mistralai/mistral-7b-instruct:free",
      systemPrompt: DEFAULT_SYSTEM_PROMPT,
      buttonLabel: "Optimize"
    },
    MESSAGE_TYPES: {
      OPTIMIZE_PROMPT: "NUKHBAPROMPT_OPTIMIZE_PROMPT"
    },
    UI: {
      ROOT_ID: "nukhba-prompt-root",
      BUTTON_ID: "nukhba-prompt-button",
      ERROR_TIMEOUT_MS: 3200
    }
  };
})(typeof globalThis !== "undefined" ? globalThis : window);
