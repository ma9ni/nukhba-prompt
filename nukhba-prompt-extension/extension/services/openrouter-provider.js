(function initOpenRouterProvider(global) {
  const OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions";

  async function optimizePrompt(config) {
    const response = await fetch(OPENROUTER_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + config.apiKey,
        "HTTP-Referer": "https://github.com/nukhbaprompt/mvp",
        "X-Title": "NukhbaPrompt"
      },
      body: JSON.stringify({
        model: config.model,
        messages: config.messages,
        temperature: 0.3
      })
    });

    const payload = await response.json().catch(function onJsonError() {
      return {};
    });

    if (!response.ok) {
      const message =
        (payload.error && payload.error.message) ||
        "OpenRouter request failed with status " + response.status + ".";
      throw new Error(message);
    }

    const content =
      payload &&
      payload.choices &&
      payload.choices[0] &&
      payload.choices[0].message &&
      payload.choices[0].message.content;

    if (!content || typeof content !== "string") {
      throw new Error("OpenRouter returned an empty optimization result.");
    }

    return content;
  }

  global.NukhbaPromptOpenRouterProvider = {
    optimizePrompt
  };
})(typeof globalThis !== "undefined" ? globalThis : self);
