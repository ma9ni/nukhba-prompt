(function initPromptOptimizer(global) {
  function buildMessages(promptText, systemPrompt) {
    return [
      {
        role: "system",
        content: systemPrompt
      },
      {
        role: "user",
        content: promptText
      }
    ];
  }

  function normalizeOptimizedPrompt(rawText) {
    let text = (rawText || "").trim();

    if (text.startsWith("```") && text.endsWith("```")) {
      text = text.replace(/^```[a-zA-Z]*\n?/, "").replace(/\n?```$/, "").trim();
    }

    if (
      (text.startsWith('"') && text.endsWith('"')) ||
      (text.startsWith("'") && text.endsWith("'"))
    ) {
      text = text.slice(1, -1).trim();
    }

    return text;
  }

  global.NukhbaPromptOptimizer = {
    buildMessages,
    normalizeOptimizedPrompt
  };
})(typeof globalThis !== "undefined" ? globalThis : self);
