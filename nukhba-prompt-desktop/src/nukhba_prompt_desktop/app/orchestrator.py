from __future__ import annotations

import logging
import threading

from PySide6.QtCore import QObject, Signal

from nukhba_prompt_desktop.services.clipboard_service import ClipboardService
from nukhba_prompt_desktop.services.notification_service import NotificationService
from nukhba_prompt_desktop.services.openrouter_service import OpenRouterService
from nukhba_prompt_desktop.services.paste_service import PasteService
from nukhba_prompt_desktop.services.prompt_optimizer import PromptOptimizerService
from nukhba_prompt_desktop.services.shortcut_service import ShortcutService
from nukhba_prompt_desktop.services.storage_service import AppSettings, StorageService
from nukhba_prompt_desktop.ui.settings_dialog import SettingsDialog
from nukhba_prompt_desktop.utils.errors import (
    ClipboardError,
    ConfigurationError,
    ProviderError,
    ShortcutRegistrationError,
)


class AppOrchestrator(QObject):
    optimization_requested = Signal()
    show_settings_requested = Signal()
    shutdown_requested = Signal()
    notify_success = Signal(str)
    notify_warning = Signal(str)
    notify_error = Signal(str)
    notify_progress = Signal(str)

    def __init__(
        self,
        logger: logging.Logger,
        storage_service: StorageService,
        clipboard_service: ClipboardService,
        openrouter_service: OpenRouterService,
        prompt_optimizer: PromptOptimizerService,
        shortcut_service: ShortcutService,
        paste_service: PasteService,
        notification_service: NotificationService,
        settings_dialog: SettingsDialog,
    ) -> None:
        super().__init__()
        self._logger = logger
        self._storage_service = storage_service
        self._clipboard_service = clipboard_service
        self._openrouter_service = openrouter_service
        self._prompt_optimizer = prompt_optimizer
        self._shortcut_service = shortcut_service
        self._paste_service = paste_service
        self._notification_service = notification_service
        self._settings_dialog = settings_dialog
        self._settings = self._storage_service.load_settings()
        self._is_running = False
        self._lock = threading.Lock()

        self.optimization_requested.connect(self.optimize_clipboard)
        self.show_settings_requested.connect(self.show_settings)
        self.notify_success.connect(self._handle_success_notification)
        self.notify_warning.connect(self._handle_warning_notification)
        self.notify_error.connect(self._handle_error_notification)
        self.notify_progress.connect(self._handle_progress_notification)
        self._settings_dialog.saved.connect(self.save_settings)

    def start(self) -> None:
        try:
            self._register_shortcut(self._settings.shortcut)
            self.notify_success.emit(
                f"NukhbaPrompt Desktop is running. Shortcut: {self._settings.shortcut}"
            )
        except ShortcutRegistrationError as exc:
            self.notify_error.emit(str(exc))

    def shutdown(self) -> None:
        self._shortcut_service.unregister()

    def trigger_optimization(self) -> None:
        self.optimization_requested.emit()

    def show_settings(self) -> None:
        self._settings_dialog.load_settings(self._settings)
        self._settings_dialog.show()
        self._settings_dialog.raise_()
        self._settings_dialog.activateWindow()

    def save_settings(self, settings: AppSettings) -> None:
        try:
            saved = self._storage_service.save_settings(settings)
            self._settings = saved
            self._register_shortcut(saved.shortcut)
            self.notify_success.emit("Settings saved.")
        except (ConfigurationError, ShortcutRegistrationError) as exc:
            self.notify_error.emit(str(exc))

    def optimize_clipboard(self) -> None:
        with self._lock:
            if self._is_running:
                self.notify_warning.emit("Optimization is already running.")
                return
            self._is_running = True

        worker = threading.Thread(target=self._run_optimization, daemon=True)
        worker.start()

    def _run_optimization(self) -> None:
        try:
            self.notify_progress.emit("Capturing selected text.")
            self._paste_service.copy_selection()
            clipboard_text = self._clipboard_service.read_text()
            self._logger.info(
                "Clipboard input preview: %s", self._build_preview(clipboard_text, 180)
            )
            if self._looks_like_internal_log_dump(clipboard_text):
                self.notify_warning.emit(
                    "Clipboard contains app logs, not the target text to optimize."
                )
                return
            self.notify_progress.emit("Waiting for OpenRouter response.")
            messages = self._prompt_optimizer.build_messages(
                clipboard_text, self._settings.system_prompt
            )
            optimized = self._openrouter_service.optimize(self._settings, messages)
            normalized = self._prompt_optimizer.normalize_response(optimized)
            if not normalized:
                raise ProviderError("The optimizer returned empty text.")

            self._clipboard_service.write_text(normalized)
            self._paste_service.paste()
            self._logger.info(
                "OpenRouter optimized output preview: %s",
                self._build_preview(normalized, 220),
            )
            self.notify_success.emit(
                "Replaced text: " + self._build_preview(normalized)
            )
        except ClipboardError as exc:
            self.notify_warning.emit(str(exc))
        except (ConfigurationError, ProviderError) as exc:
            self.notify_error.emit(str(exc))
        except Exception as exc:  # pragma: no cover
            self._logger.exception("Unexpected optimization failure")
            self.notify_error.emit(f"Unexpected error: {exc}")
        finally:
            with self._lock:
                self._is_running = False

    def _register_shortcut(self, shortcut: str) -> None:
        self._shortcut_service.update_shortcut(shortcut, self.trigger_optimization)

    def _handle_success_notification(self, message: str) -> None:
        self._notification_service.success(message, self._settings.notifications_enabled)

    def _handle_warning_notification(self, message: str) -> None:
        self._notification_service.warning(message, self._settings.notifications_enabled)

    def _handle_error_notification(self, message: str) -> None:
        self._notification_service.error(message, self._settings.notifications_enabled)

    def _handle_progress_notification(self, message: str) -> None:
        self._notification_service.progress(message, self._settings.notifications_enabled)

    @staticmethod
    def _build_preview(text: str, max_length: int = 120) -> str:
        single_line = " ".join(text.split())
        if len(single_line) <= max_length:
            return single_line
        return single_line[: max_length - 3] + "..."

    @staticmethod
    def _looks_like_internal_log_dump(text: str) -> bool:
        lowered = text.lower()
        markers = (
            "nukhbaprompt desktop",
            "clipboard input",
            "openrouter optimized output",
            "registered global shortcut",
            "application started. shortcut",
        )
        hits = sum(1 for marker in markers if marker in lowered)
        return hits >= 2
