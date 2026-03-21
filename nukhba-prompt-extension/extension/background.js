importScripts(
  "utils/constants.js",
  "utils/storage.js",
  "services/prompt-optimizer.js",
  "services/openrouter-provider.js"
);

chrome.runtime.onInstalled.addListener(function onInstalled() {
  chrome.storage.local.get(NukhbaPromptConstants.DEFAULTS, function ensureDefaults(items) {
    const nextValues = {};
    Object.keys(NukhbaPromptConstants.DEFAULTS).forEach(function maybeFillDefault(key) {
      if (typeof items[key] === "undefined") {
        nextValues[key] = NukhbaPromptConstants.DEFAULTS[key];
      }
    });

    if (Object.keys(nextValues).length > 0) {
      chrome.storage.local.set(nextValues);
    }
  });
});

chrome.runtime.onMessage.addListener(function onMessage(message, sender, sendResponse) {
  if (!message || message.type !== NukhbaPromptConstants.MESSAGE_TYPES.OPTIMIZE_PROMPT) {
    return false;
  }

  handleOptimizationRequest(message, sender)
    .then(function onSuccess(result) {
      sendResponse({ ok: true, optimizedPrompt: result });
    })
    .catch(function onError(error) {
      sendResponse({
        ok: false,
        error: error && error.message ? error.message : "Prompt optimization failed."
      });
    });

  return true;
});

async function handleOptimizationRequest(message) {
  const promptText = (message.prompt || "").trim();
  if (!promptText) {
    throw new Error("No prompt found to optimize.");
  }

  const settings = await NukhbaPromptStorage.getSettings();
  if (!settings.openrouterApiKey) {
    throw new Error("OpenRouter API key is missing. Add it in the NukhbaPrompt options page.");
  }

  if (!settings.openrouterModel) {
    throw new Error("OpenRouter model is missing. Configure it in the options page.");
  }

  const messages = NukhbaPromptOptimizer.buildMessages(promptText, settings.systemPrompt);
  const rawResponse = await NukhbaPromptOpenRouterProvider.optimizePrompt({
    apiKey: settings.openrouterApiKey,
    model: settings.openrouterModel,
    messages: messages
  });

  const optimizedPrompt = NukhbaPromptOptimizer.normalizeOptimizedPrompt(rawResponse);
  if (!optimizedPrompt) {
    throw new Error("The optimizer returned an empty prompt.");
  }

  return optimizedPrompt;
}
