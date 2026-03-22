from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from nukhba_prompt_desktop.app.orchestrator import AppOrchestrator
from nukhba_prompt_desktop.services.clipboard_service import ClipboardService
from nukhba_prompt_desktop.services.notification_service import NotificationService
from nukhba_prompt_desktop.services.openrouter_service import OpenRouterService
from nukhba_prompt_desktop.services.paste_service import PasteService
from nukhba_prompt_desktop.services.prompt_optimizer import PromptOptimizerService
from nukhba_prompt_desktop.services.shortcut_service import ShortcutService
from nukhba_prompt_desktop.services.storage_service import StorageService
from nukhba_prompt_desktop.ui.settings_dialog import SettingsDialog
from nukhba_prompt_desktop.ui.tray import create_tray
from nukhba_prompt_desktop.utils.logger import setup_logger


def main() -> int:
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(Path.cwd() / ".env", override=True)
    load_dotenv(project_root / ".env", override=True)
    logger = setup_logger()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("NukhbaPrompt Desktop")

    storage_service = StorageService()
    clipboard_service = ClipboardService()
    openrouter_service = OpenRouterService()
    paste_service = PasteService()
    prompt_optimizer = PromptOptimizerService()
    shortcut_service = ShortcutService(logger)
    settings_dialog = SettingsDialog()
    notification_service = NotificationService(logger)

    orchestrator = AppOrchestrator(
        logger=logger,
        storage_service=storage_service,
        clipboard_service=clipboard_service,
        openrouter_service=openrouter_service,
        prompt_optimizer=prompt_optimizer,
        shortcut_service=shortcut_service,
        paste_service=paste_service,
        notification_service=notification_service,
        settings_dialog=settings_dialog,
    )

    tray = create_tray(
        on_optimize=lambda: orchestrator.trigger_optimization("optimize"),
        on_enhanced=lambda: orchestrator.trigger_optimization("enhanced"),
        on_summarize=lambda: orchestrator.trigger_optimization("summarize"),
        on_translate=lambda: orchestrator.trigger_optimization("translate"),
        on_reply=lambda: orchestrator.trigger_optimization("reply"),
        on_grammar=lambda: orchestrator.trigger_optimization("grammar"),
        on_settings=orchestrator.show_settings_requested.emit,
        on_quit=app.quit,
    )
    tray.show()
    notification_service.set_tray_icon(tray)

    app.aboutToQuit.connect(orchestrator.shutdown)
    orchestrator.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
