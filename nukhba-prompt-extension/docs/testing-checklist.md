# NukhbaPrompt Testing Checklist

## Setup

- Load the `extension/` folder as an unpacked extension in Chrome.
- Open the extension options page.
- Add a valid OpenRouter API key.
- Confirm the selected model exists and is accessible.

## Configuration

- Save settings with all fields populated.
- Restore defaults and verify the default system prompt reappears.
- Change the button label and confirm the inline label updates on supported pages.

## ChatGPT

- Open `https://chatgpt.com/`.
- Confirm the Optimize button appears near the active prompt field.
- Type text into the prompt area and click Optimize.
- Verify the prompt is replaced with the optimized version.
- Confirm the button shows `Optimizing...` while the request is in flight.
- Confirm the button is disabled during the request.

## Claude

- Open `https://claude.ai/`.
- Confirm the Optimize button appears near the active prompt field.
- Type text into the prompt area and click Optimize.
- Verify the optimized prompt replaces the original prompt.

## Prompt Detection

- Test a standard `textarea`.
- Test a `contenteditable` prompt surface.
- Test a field using `role="textbox"`.
- Confirm the active field changes when focus moves between multiple candidates.

## Error Cases

- Remove the API key and confirm the inline error message appears.
- Clear the prompt field and confirm `No prompt found.` appears.
- Use an invalid model and confirm the OpenRouter error is shown.
- Disconnect the network and confirm a request error is shown.

## Regression Checks

- Refresh ChatGPT and Claude after navigation and confirm the button still appears.
- Scroll the page and confirm the button continues to track the active prompt field.
- Resize the viewport and confirm the button repositions correctly.
- Verify the options page remains usable on a narrow viewport.
