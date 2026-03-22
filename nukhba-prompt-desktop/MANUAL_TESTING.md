# Manual Testing Guide

## Startup

1. Create and activate a virtual environment.
2. Install the project in editable mode with dev dependencies:
   `pip install -e .[dev]`
3. Copy `.env.example` to `.env` if you want bootstrap values.
4. Run:
   `python -m nukhba_prompt_desktop.main`

## Settings

1. Open the tray menu.
2. Click `Settings`.
3. Enter:
   - OpenRouter API key
   - model
   - shortcut
   - system prompt
4. Save and confirm you see a success notification.

## Clipboard Shortcut Flow

1. Open any desktop text app such as Notepad, Teams, Outlook, or Word.
2. Write a short prompt or rough instruction.
3. Copy the text.
4. Press `Ctrl+Shift+O`.
5. Wait for the success notification.
6. Paste and confirm the clipboard now contains the optimized version.

## Error Cases

- Empty clipboard: press the shortcut with no text copied and confirm a warning appears.
- Missing API key: clear the key in settings and confirm an error appears on optimization.
- Invalid model: set a bad model name and confirm the provider error appears.
- Duplicate press: press the shortcut repeatedly and confirm only one optimization runs at a time.

## Tray

- Click `Optimize Clipboard` from the tray menu and confirm it triggers the same workflow.
- Click `Quit` and confirm the app exits cleanly.
