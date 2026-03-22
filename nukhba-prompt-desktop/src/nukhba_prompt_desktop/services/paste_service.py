from __future__ import annotations

import platform
import time

from pynput.keyboard import Controller, Key


class PasteService:
    def __init__(self, settle_delay_seconds: float = 0.12, copy_delay_seconds: float = 0.18) -> None:
        self._keyboard = Controller()
        self._settle_delay_seconds = settle_delay_seconds
        self._copy_delay_seconds = copy_delay_seconds

    def copy_selection(self) -> None:
        modifier = Key.cmd if platform.system() == "Darwin" else Key.ctrl
        with self._keyboard.pressed(modifier):
            self._keyboard.press("c")
            self._keyboard.release("c")
        time.sleep(self._copy_delay_seconds)

    def paste(self) -> None:
        time.sleep(self._settle_delay_seconds)
        modifier = Key.cmd if platform.system() == "Darwin" else Key.ctrl
        with self._keyboard.pressed(modifier):
            self._keyboard.press("v")
            self._keyboard.release("v")
