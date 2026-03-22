from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from nukhba_prompt_desktop.services.storage_service import AppSettings, DEFAULT_SHORTCUTS
from nukhba_prompt_desktop.utils.errors import ConfigurationError


class SettingsDialog(QDialog):
    saved = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NukhbaPrompt Settings")
        self.setMinimumSize(760, 760)

        self._api_key_input = QLineEdit()
        self._api_key_input.setEchoMode(QLineEdit.Password)
        self._model_input = QLineEdit()
        self._notifications_checkbox = QCheckBox("Enable desktop notifications")
        self._shortcut_inputs = {
            action: QLineEdit() for action in DEFAULT_SHORTCUTS
        }
        self._profile_role_input = QLineEdit()
        self._profile_domains_input = QLineEdit()
        self._preferred_language_input = QLineEdit()
        self._writing_preferences_input = QPlainTextEdit()
        self._writing_preferences_input.setMinimumHeight(90)
        self._additional_context_input = QPlainTextEdit()
        self._additional_context_input.setMinimumHeight(120)
        self._rules_input = QPlainTextEdit()
        self._rules_input.setMinimumHeight(120)
        self._system_prompt_input = QPlainTextEdit()
        self._system_prompt_input.setMinimumHeight(220)

        description = QLabel(
            "Configure the desktop assistant: shortcuts, user profile, rules, extra context, and the base system prompt."
        )
        description.setWordWrap(True)

        api_group = QGroupBox("Provider")
        api_layout = QFormLayout()
        api_layout.addRow("OpenRouter API key", self._api_key_input)
        api_layout.addRow("Model", self._model_input)
        api_layout.addRow("", self._notifications_checkbox)
        api_group.setLayout(api_layout)

        shortcuts_group = QGroupBox("Shortcuts")
        shortcuts_layout = QFormLayout()
        shortcuts_layout.addRow("Optimize", self._shortcut_inputs["optimize"])
        shortcuts_layout.addRow("Summarize", self._shortcut_inputs["summarize"])
        shortcuts_layout.addRow("Translate", self._shortcut_inputs["translate"])
        shortcuts_layout.addRow("Reply", self._shortcut_inputs["reply"])
        shortcuts_layout.addRow("Grammar fix", self._shortcut_inputs["grammar"])
        shortcuts_group.setLayout(shortcuts_layout)

        profile_group = QGroupBox("Profile and Context")
        profile_layout = QFormLayout()
        profile_layout.addRow("Role", self._profile_role_input)
        profile_layout.addRow("Domains", self._profile_domains_input)
        profile_layout.addRow("Preferred language", self._preferred_language_input)
        profile_layout.addRow("Writing preferences", self._writing_preferences_input)
        profile_layout.addRow("Additional context", self._additional_context_input)
        profile_layout.addRow("Rules", self._rules_input)
        profile_group.setLayout(profile_layout)

        prompt_group = QGroupBox("Prompt Assembly")
        prompt_layout = QFormLayout()
        prompt_layout.addRow("System prompt", self._system_prompt_input)
        prompt_group.setLayout(prompt_layout)

        self._button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        self._button_box.accepted.connect(self._on_save)
        self._button_box.rejected.connect(self.hide)

        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.addWidget(description)
        content_layout.addWidget(api_group)
        content_layout.addWidget(shortcuts_group)
        content_layout.addWidget(profile_group)
        content_layout.addWidget(prompt_group)
        content_layout.addWidget(self._button_box)
        content.setLayout(content_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        self.setLayout(layout)

    def load_settings(self, settings: AppSettings) -> None:
        self._api_key_input.setText(settings.openrouter_api_key)
        self._model_input.setText(settings.openrouter_model)
        for action, widget in self._shortcut_inputs.items():
            widget.setText(settings.shortcuts.get(action, DEFAULT_SHORTCUTS[action]))
        self._notifications_checkbox.setChecked(settings.notifications_enabled)
        self._profile_role_input.setText(settings.profile_role)
        self._profile_domains_input.setText(settings.profile_domains)
        self._preferred_language_input.setText(settings.preferred_language)
        self._writing_preferences_input.setPlainText(settings.writing_preferences)
        self._additional_context_input.setPlainText(settings.additional_context)
        self._rules_input.setPlainText(settings.rules_text)
        self._system_prompt_input.setPlainText(settings.system_prompt)

    def _on_save(self) -> None:
        settings = AppSettings(
            openrouter_api_key=self._api_key_input.text().strip(),
            openrouter_model=self._model_input.text().strip(),
            system_prompt=self._system_prompt_input.toPlainText().strip(),
            shortcuts={
                action: widget.text().strip()
                for action, widget in self._shortcut_inputs.items()
            },
            notifications_enabled=self._notifications_checkbox.isChecked(),
            profile_role=self._profile_role_input.text().strip(),
            profile_domains=self._profile_domains_input.text().strip(),
            preferred_language=self._preferred_language_input.text().strip(),
            writing_preferences=self._writing_preferences_input.toPlainText().strip(),
            additional_context=self._additional_context_input.toPlainText().strip(),
            rules_text=self._rules_input.toPlainText().strip(),
        )

        try:
            settings.validate()
        except ConfigurationError as exc:
            QMessageBox.warning(self, "Invalid settings", str(exc))
            return

        self.saved.emit(settings)
        self.hide()
