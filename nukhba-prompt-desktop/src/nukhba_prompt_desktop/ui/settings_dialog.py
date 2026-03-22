from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QVBoxLayout,
)

from nukhba_prompt_desktop.services.storage_service import AppSettings
from nukhba_prompt_desktop.utils.errors import ConfigurationError


class SettingsDialog(QDialog):
    saved = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NukhbaPrompt Settings")
        self.setMinimumWidth(560)

        self._api_key_input = QLineEdit()
        self._api_key_input.setEchoMode(QLineEdit.Password)
        self._model_input = QLineEdit()
        self._shortcut_input = QLineEdit()
        self._notifications_checkbox = QCheckBox("Enable desktop notifications")
        self._system_prompt_input = QPlainTextEdit()
        self._system_prompt_input.setMinimumHeight(220)

        description = QLabel(
            "Shortcut-first utility: copy text, press the global shortcut, then paste the optimized result."
        )
        description.setWordWrap(True)

        form_layout = QFormLayout()
        form_layout.addRow("OpenRouter API key", self._api_key_input)
        form_layout.addRow("Model", self._model_input)
        form_layout.addRow("Shortcut", self._shortcut_input)
        form_layout.addRow("", self._notifications_checkbox)
        form_layout.addRow("System prompt", self._system_prompt_input)

        self._button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        self._button_box.accepted.connect(self._on_save)
        self._button_box.rejected.connect(self.hide)

        layout = QVBoxLayout()
        layout.addWidget(description)
        layout.addLayout(form_layout)
        layout.addWidget(self._button_box)
        self.setLayout(layout)

    def load_settings(self, settings: AppSettings) -> None:
        self._api_key_input.setText(settings.openrouter_api_key)
        self._model_input.setText(settings.openrouter_model)
        self._shortcut_input.setText(settings.shortcut)
        self._notifications_checkbox.setChecked(settings.notifications_enabled)
        self._system_prompt_input.setPlainText(settings.system_prompt)

    def _on_save(self) -> None:
        settings = AppSettings(
            openrouter_api_key=self._api_key_input.text().strip(),
            openrouter_model=self._model_input.text().strip(),
            system_prompt=self._system_prompt_input.toPlainText().strip(),
            shortcut=self._shortcut_input.text().strip(),
            notifications_enabled=self._notifications_checkbox.isChecked(),
        )

        try:
            settings.validate()
        except ConfigurationError as exc:
            QMessageBox.warning(self, "Invalid settings", str(exc))
            return

        self.saved.emit(settings)
        self.hide()
