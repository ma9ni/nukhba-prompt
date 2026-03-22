# NukhbaPrompt Desktop

NukhbaPrompt Desktop is a lightweight Python utility that optimizes clipboard text with a global shortcut.

It is designed for desktop applications where browser extensions cannot run, such as Microsoft Teams Desktop, Outlook Desktop, Word, and Notepad.

The core workflow is:

1. Copy text from any desktop app.
2. Press the global shortcut.
3. NukhbaPrompt Desktop sends the clipboard text to OpenRouter.
4. The optimized result is written back to the clipboard.
5. Paste the improved version anywhere.

## Architecture

The MVP is organized around isolated services:

- `ShortcutService`: registers a real global hotkey through `pynput`.
- `ClipboardService`: reads and writes plain-text clipboard content through `pyperclip`.
- `OpenRouterService`: sends chat-completion requests to OpenRouter.
- `PromptOptimizerService`: builds request messages and normalizes responses.
- `NotificationService`: uses tray notifications and logging.
- `StorageService`: persists settings locally as JSON and supports `.env` bootstrap values.
- `AppOrchestrator`: coordinates shortcut event → clipboard read → optimize → clipboard write → notify.

## Implementation Plan

### Phase 1

- set up the Python package and settings model
- add clipboard, provider, and prompt normalization services

### Phase 2

- implement the global shortcut listener
- add the orchestrator and duplicate-trigger protection

### Phase 3

- add the tray menu, notifications, and settings dialog
- add docs and a minimal test suite

## Project Tree

```text
nukhba-prompt-desktop/
├── AGENTS.md
├── .env.example
├── MANUAL_TESTING.md
├── README.md
├── pyproject.toml
├── src/
│   └── nukhba_prompt_desktop/
│       ├── __init__.py
│       ├── main.py
│       ├── app/
│       │   └── orchestrator.py
│       ├── services/
│       │   ├── clipboard_service.py
│       │   ├── notification_service.py
│       │   ├── openrouter_service.py
│       │   ├── prompt_optimizer.py
│       │   ├── shortcut_service.py
│       │   └── storage_service.py
│       ├── ui/
│       │   ├── settings_dialog.py
│       │   └── tray.py
│       └── utils/
│           ├── errors.py
│           └── logger.py
└── tests/
    ├── test_prompt_optimizer.py
    └── test_storage_service.py
```

## Quick Start

1. Create a virtual environment.
2. Install the project:
   `pip install -e .`
3. Run the app:
   `python -m nukhba_prompt_desktop.main`
4. Open the tray menu and configure:
   - OpenRouter API key
   - model
   - shortcut
   - system prompt

## Settings Persistence

Settings are saved per platform:

- Linux: `~/.config/nukhba_prompt_desktop/settings.json`
- Windows: `%APPDATA%\\nukhba_prompt_desktop\\settings.json`
- macOS: `~/Library/Application Support/nukhba_prompt_desktop/settings.json`

The app also reads optional bootstrap values from `.env`.

## Notifications

Notifications are shown through the system tray when supported by the platform. The same events are also written to the app log.

## Manual Testing

See [MANUAL_TESTING.md](/home/ahmed/IdeaProjects/nukhba-prompt/nukhba-prompt-desktop/MANUAL_TESTING.md).

## Cross-Platform Status

Current target support:

- Linux: supported, best on X11
- Windows: supported for tray, clipboard, and global shortcuts
- macOS: partially supported, but usually requires Accessibility permissions for global hotkeys and synthetic paste

## Platform Limitations

- Global hotkeys depend on `pynput`, which may require Accessibility permissions on macOS.
- On Linux, global hotkeys usually require an X11 session; Wayland support can be limited depending on the desktop environment.
- Clipboard access uses Qt first and falls back to `pyperclip`, which improves cross-platform behavior.
- Tray notifications depend on desktop-environment support and may vary by platform.
- Synthetic copy/paste is best effort. Some native applications may block or ignore simulated key events.

## Next Improvements

- shortcut capture widget instead of plain text entry
- richer provider retry logic
- clipboard history
- startup-on-login support
- packaged binaries with PyInstaller
