from __future__ import annotations

import pyperclip
from PySide6.QtGui import QClipboard, QGuiApplication

from nukhba_prompt_desktop.utils.errors import ClipboardError


class ClipboardService:
    def read_text(self) -> str:
        value = self._read_native_clipboard()

        text = value.strip()
        if not text:
            raise ClipboardError("Clipboard is empty.")
        return text

    def write_text(self, value: str) -> None:
        text = (value or "").strip()
        if not text:
            raise ClipboardError("Cannot write empty text to the clipboard.")
        self._write_native_clipboard(text)

    @staticmethod
    def _read_native_clipboard() -> str:
        clipboard = QGuiApplication.clipboard()
        value = clipboard.text(mode=QClipboard.Mode.Clipboard)
        if isinstance(value, str):
            return value

        if clipboard.supportsSelection():
            selection_value = clipboard.text(mode=QClipboard.Mode.Selection)
            if isinstance(selection_value, str):
                return selection_value

        try:
            fallback = pyperclip.paste()
        except pyperclip.PyperclipException as exc:
            raise ClipboardError(
                "Clipboard access is unavailable on this system."
            ) from exc

        if not isinstance(fallback, str):
            raise ClipboardError("Clipboard content is not plain text.")
        return fallback

    @staticmethod
    def _write_native_clipboard(value: str) -> None:
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(value, mode=QClipboard.Mode.Clipboard)
        if clipboard.supportsSelection():
            clipboard.setText(value, mode=QClipboard.Mode.Selection)

        if clipboard.text(mode=QClipboard.Mode.Clipboard) == value:
            return

        try:
            pyperclip.copy(value)
        except pyperclip.PyperclipException as exc:
            raise ClipboardError(
                "Clipboard write is unavailable on this system."
            ) from exc
