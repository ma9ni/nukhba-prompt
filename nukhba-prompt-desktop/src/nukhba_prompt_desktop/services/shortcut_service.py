from __future__ import annotations

import logging
import time
from collections.abc import Callable

from pynput import keyboard

from nukhba_prompt_desktop.utils.errors import ShortcutRegistrationError


class ShortcutService:
    def __init__(self, logger: logging.Logger, debounce_seconds: float = 0.8) -> None:
        self._logger = logger
        self._debounce_seconds = debounce_seconds
        self._listener: keyboard.GlobalHotKeys | None = None
        self._callback: Callable[[], None] | None = None
        self._last_trigger_at = 0.0

    def register(self, shortcut: str, callback: Callable[[], None]) -> None:
        sequence = self._to_pynput_sequence(shortcut)
        self.unregister()
        self._callback = callback

        try:
            self._listener = keyboard.GlobalHotKeys({sequence: self._on_trigger})
            self._listener.start()
            self._logger.info("Registered global shortcut %s as %s", shortcut, sequence)
        except Exception as exc:
            raise ShortcutRegistrationError(
                f"Could not register shortcut '{shortcut}'."
            ) from exc

    def unregister(self) -> None:
        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    def update_shortcut(self, shortcut: str, callback: Callable[[], None]) -> None:
        self.register(shortcut, callback)

    def _on_trigger(self) -> None:
        now = time.monotonic()
        if now - self._last_trigger_at < self._debounce_seconds:
            self._logger.debug("Ignored duplicate shortcut trigger.")
            return

        self._last_trigger_at = now
        if self._callback is not None:
            self._callback()

    @staticmethod
    def _to_pynput_sequence(shortcut: str) -> str:
        parts = [part.strip().lower() for part in shortcut.split("+") if part.strip()]
        if not parts:
            raise ShortcutRegistrationError("Shortcut cannot be empty.")

        mapped_parts: list[str] = []
        key_map = {
            "ctrl": "<ctrl>",
            "control": "<ctrl>",
            "shift": "<shift>",
            "alt": "<alt>",
            "option": "<alt>",
            "cmd": "<cmd>",
            "command": "<cmd>",
            "meta": "<cmd>",
            "super": "<cmd>",
        }

        for part in parts:
            if part in key_map:
                mapped_parts.append(key_map[part])
            elif len(part) == 1 and part.isprintable():
                mapped_parts.append(part)
            elif part.startswith("f") and part[1:].isdigit():
                mapped_parts.append(f"<{part}>")
            else:
                raise ShortcutRegistrationError(f"Unsupported shortcut key: {part}")

        return "+".join(mapped_parts)
