# NukhbaPrompt

NukhbaPrompt is a Chrome extension that improves prompts directly inside AI tools such as ChatGPT and Claude.

The MVP adds a small inline `Optimize` button next to the active prompt field. When clicked, it reads the current prompt, sends it to OpenRouter with a configurable system prompt, and replaces the original text with a clearer, more structured version.

## MVP Deliverables

- Manifest V3 Chrome extension
- ChatGPT and Claude support
- Inline Optimize button near the active prompt field
- Background-script OpenRouter integration
- Configurable API key, model, system prompt, and button label
- Options page for configuration
- Minimal loading and error states

## Architecture Proposal

The MVP is intentionally simple:

- `content.js` handles prompt detection, button placement, prompt read/write, and user feedback.
- `background.js` receives optimization requests, loads configuration, and calls OpenRouter.
- `services/prompt-optimizer.js` builds messages and normalizes the returned text.
- `services/openrouter-provider.js` sends the HTTP request to OpenRouter.
- `utils/` contains shared constants, DOM helpers, and storage helpers.

This keeps the extension readable and avoids framework or build-step overhead.

## Implementation Plan

### Phase 1

- Create the extension structure and constants
- Define storage defaults and settings persistence
- Set up Manifest V3 permissions and routes

### Phase 2

- Implement background messaging
- Build the OpenRouter provider
- Build the prompt optimizer service

### Phase 3

- Detect supported prompt fields on ChatGPT and Claude
- Inject the inline Optimize button
- Read and replace prompt content reliably

### Phase 4

- Add the options page
- Add loading, disabled, and error states
- Write docs and testing checklist

## File Tree

```text
nukhba-prompt/
├── AGENTS.md
├── PR.md
├── README.md
├── docs/
│   ├── mvp-architecture.md
│   └── testing-checklist.md
└── extension/
    ├── background.js
    ├── content.js
    ├── manifest.json
    ├── options.html
    ├── options.js
    ├── styles.css
    ├── icons/
    │   └── nukhba-mark.svg
    ├── services/
    │   ├── openrouter-provider.js
    │   └── prompt-optimizer.js
    └── utils/
        ├── constants.js
        ├── dom.js
        └── storage.js
```

## Setup

1. Open Chrome and go to `chrome://extensions`.
2. Enable Developer mode.
3. Click `Load unpacked`.
4. Select the [`extension/`](/home/ahmed/IdeaProjects/nukhba-prompt/extension) directory.
5. Open the extension options page.
6. Add:
   - OpenRouter API key
   - OpenRouter model
   - Optional custom button label
   - Optional custom system prompt

## Default System Prompt

```text
You are an expert prompt engineer.

Your job is to rewrite the user's prompt so it becomes clearer, more precise, and more effective for AI systems such as ChatGPT or Claude.

Rules:
- Preserve the original intent
- Do not answer the user's request
- Do not add explanations
- Do not wrap the result in quotes
- Return only the improved prompt text
- Make the prompt more structured, specific, and actionable
- If the original prompt is already good, improve it slightly without overcomplicating it
```

## Notes

- The default model is configurable and can be changed from the options page without code edits.
- For MVP speed, the OpenRouter API key is stored in `chrome.storage.local`.
- If a model becomes unavailable on OpenRouter, update it in the options page.

## Documentation

- Architecture: [docs/mvp-architecture.md](/home/ahmed/IdeaProjects/nukhba-prompt/docs/mvp-architecture.md)
- Testing checklist: [docs/testing-checklist.md](/home/ahmed/IdeaProjects/nukhba-prompt/docs/testing-checklist.md)
