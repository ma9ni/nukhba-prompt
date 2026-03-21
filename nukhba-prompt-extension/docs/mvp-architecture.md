# NukhbaPrompt MVP Architecture

## Goal

NukhbaPrompt is a Manifest V3 Chrome extension that upgrades weak prompts inline inside ChatGPT and Claude with one click.

## Architecture Summary

The MVP uses three layers:

1. `content.js`
   Detects prompt inputs, anchors the inline button near the active field, reads the current prompt, and writes the optimized prompt back into the page.

2. `background.js`
   Acts as the privileged broker between the content script and OpenRouter. It loads settings from `chrome.storage.local`, validates them, and returns the optimized prompt.

3. `services/`
   Encapsulates optimization logic and OpenRouter HTTP calls so API concerns stay out of both the content layer and the options page.

## Runtime Flow

1. The content script runs on `chatgpt.com`, `chat.openai.com`, and `claude.ai`.
2. It scans for supported prompt fields:
   - `textarea`
   - `[contenteditable="true"]`
   - `[contenteditable="plaintext-only"]`
   - `[role="textbox"]`
3. When a supported field is focused, NukhbaPrompt shows a fixed-position inline button near that field.
4. On click, the content script reads the prompt and sends it to the background worker through `chrome.runtime.sendMessage`.
5. The background script loads:
   - `openrouterApiKey`
   - `openrouterModel`
   - `systemPrompt`
   - `buttonLabel`
6. The background script builds the OpenRouter chat payload and sends the request.
7. The optimized prompt text is returned to the content script.
8. The content script replaces the current prompt value and dispatches `input` and `change` events so host apps react correctly.

## Storage Model

The extension stores configuration in `chrome.storage.local`:

- `openrouterApiKey`
- `openrouterModel`
- `systemPrompt`
- `buttonLabel`

Defaults are initialized on install and can be restored from the options page.

## Design Decisions

### Single Floating Button

Instead of injecting a button into each host app's internal DOM structure, the MVP uses one fixed-position button that follows the active prompt field. This avoids fragile per-site selectors and makes the extension more resilient to ChatGPT and Claude UI changes.

### Classic Background Service Worker

The background worker uses `importScripts` with plain JavaScript globals instead of modules. This keeps the MVP simple and avoids bundling.

### Minimal Service Layer

`prompt-optimizer.js` handles prompt-message construction and output cleanup.

`openrouter-provider.js` handles HTTP concerns only.

This keeps responsibilities separated without introducing premature abstraction.

## Error Handling

The MVP surfaces clear inline errors for:

- missing API key
- missing model
- empty prompt
- network or OpenRouter request failures
- empty model responses

## Limitations

- API keys are stored locally in the browser for MVP speed, not production security.
- Contenteditable editors can differ internally; the current implementation aims for broad compatibility, not host-specific perfection.
- The extension currently targets ChatGPT and Claude only.

## Next Logical Enhancements

- per-site prompt strategies
- prompt history and restore
- host-specific adapters for richer editor support
- backend proxy for API key protection
- richer button placement heuristics
