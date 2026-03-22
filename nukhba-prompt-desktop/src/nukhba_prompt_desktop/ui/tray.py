from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon


def create_tray(
    on_optimize,
    on_settings,
    on_quit,
) -> QSystemTrayIcon:
    app = QApplication.instance()
    icon = app.style().standardIcon(QStyle.SP_ComputerIcon)

    tray = QSystemTrayIcon(icon)
    tray.setToolTip("NukhbaPrompt Desktop")

    menu = QMenu()

    optimize_action = QAction("Optimize Clipboard")
    optimize_action.triggered.connect(on_optimize)
    menu.addAction(optimize_action)

    settings_action = QAction("Settings")
    settings_action.triggered.connect(on_settings)
    menu.addAction(settings_action)

    menu.addSeparator()

    quit_action = QAction("Quit")
    quit_action.triggered.connect(on_quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.activated.connect(lambda reason: on_optimize() if reason == QSystemTrayIcon.Trigger else None)
    return tray
