from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon


def create_tray(
    on_optimize,
    on_summarize,
    on_translate,
    on_reply,
    on_grammar,
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

    summarize_action = QAction("Summarize Clipboard")
    summarize_action.triggered.connect(on_summarize)
    menu.addAction(summarize_action)

    translate_action = QAction("Translate Clipboard")
    translate_action.triggered.connect(on_translate)
    menu.addAction(translate_action)

    reply_action = QAction("Reply Professionally")
    reply_action.triggered.connect(on_reply)
    menu.addAction(reply_action)

    grammar_action = QAction("Fix Grammar")
    grammar_action.triggered.connect(on_grammar)
    menu.addAction(grammar_action)

    menu.addSeparator()

    settings_action = QAction("Settings")
    settings_action.triggered.connect(on_settings)
    menu.addAction(settings_action)

    menu.addSeparator()

    quit_action = QAction("Quit")
    quit_action.triggered.connect(on_quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.activated.connect(
        lambda reason: on_settings()
        if reason in {QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick}
        else None
    )
    return tray
