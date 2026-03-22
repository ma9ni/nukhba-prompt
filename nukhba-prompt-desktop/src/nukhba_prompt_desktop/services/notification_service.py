from __future__ import annotations

import logging

from PySide6.QtWidgets import QSystemTrayIcon


class NotificationService:
    def __init__(self, logger: logging.Logger, tray_icon: QSystemTrayIcon | None = None) -> None:
        self._logger = logger
        self._tray_icon = tray_icon

    def set_tray_icon(self, tray_icon: QSystemTrayIcon) -> None:
        self._tray_icon = tray_icon

    def notify(self, title: str, message: str, enabled: bool = True, icon: QSystemTrayIcon.MessageIcon | None = None) -> None:
        self._logger.info("%s | %s", title, message)
        if self._tray_icon is not None:
            self._tray_icon.setToolTip(f"{title} | {message}")
        if enabled and self._tray_icon is not None and self._tray_icon.supportsMessages():
            self._tray_icon.showMessage(title, message, icon or QSystemTrayIcon.Information, 3500)

    def progress(self, message: str, enabled: bool = True) -> None:
        self.notify("NukhbaPrompt", "Optimizing... " + message, enabled, QSystemTrayIcon.Information)

    def success(self, message: str, enabled: bool = True) -> None:
        self.notify("NukhbaPrompt", message, enabled, QSystemTrayIcon.Information)

    def warning(self, message: str, enabled: bool = True) -> None:
        self.notify("NukhbaPrompt", message, enabled, QSystemTrayIcon.Warning)

    def error(self, message: str, enabled: bool = True) -> None:
        self.notify("NukhbaPrompt", message, enabled, QSystemTrayIcon.Critical)
