from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from nukhba_prompt_desktop.utils.errors import ConfigurationError
from nukhba_prompt_desktop.utils.paths import get_app_data_dir


DEFAULT_SYSTEM_PROMPT = """You are an expert prompt engineer.

Your job is to rewrite the user's text so it becomes clearer, more precise, and more effective for AI systems such as ChatGPT or Claude.

Rules:
- Preserve the original intent
- Do not answer the user's request
- Do not add explanations
- Do not wrap the result in quotes
- Return only the improved prompt text
- Make the prompt more structured, specific, and actionable
- If the original text is already good, improve it slightly without overcomplicating it
"""

DEFAULT_SHORTCUTS = {
    "optimize": "Ctrl+Shift+O",
    "summarize": "Ctrl+Shift+S",
    "translate": "Ctrl+Shift+T",
    "reply": "Ctrl+Shift+R",
    "grammar": "Ctrl+Shift+G",
}


@dataclass(slots=True)
class AppSettings:
    openrouter_api_key: str = ""
    openrouter_model: str = "mistralai/mistral-7b-instruct:free"
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    shortcuts: dict[str, str] | None = None
    notifications_enabled: bool = True
    profile_role: str = ""
    profile_domains: str = ""
    preferred_language: str = ""
    writing_preferences: str = ""
    additional_context: str = ""
    rules_text: str = ""

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["shortcuts"] = self.shortcuts or DEFAULT_SHORTCUTS.copy()
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "AppSettings":
        data = cls().to_dict()
        data.update({key: value for key, value in payload.items() if key in data})
        data["shortcuts"] = DEFAULT_SHORTCUTS.copy() | dict(payload.get("shortcuts", {}))

        legacy_shortcut = payload.get("shortcut")
        if isinstance(legacy_shortcut, str) and legacy_shortcut.strip():
            data["shortcuts"]["optimize"] = legacy_shortcut.strip()

        notifications_enabled = data.get("notifications_enabled", True)
        if isinstance(notifications_enabled, str):
            notifications_enabled = notifications_enabled.strip().lower() in {"1", "true", "yes", "on"}
        data["notifications_enabled"] = bool(notifications_enabled)

        return cls(**data)

    def validate(self) -> None:
        if not self.openrouter_model.strip():
            raise ConfigurationError("Model name is required.")
        if not self.system_prompt.strip():
            raise ConfigurationError("System prompt is required.")
        for action, shortcut in (self.shortcuts or {}).items():
            if not str(shortcut).strip():
                raise ConfigurationError(f"Shortcut is required for {action}.")


class StorageService:
    def __init__(self, base_dir: Path | None = None) -> None:
        self._config_dir = base_dir or get_app_data_dir()
        self._settings_path = self._config_dir / "settings.json"

    @property
    def settings_path(self) -> Path:
        return self._settings_path

    def load_settings(self) -> AppSettings:
        data: dict[str, object] = {}
        if self._settings_path.exists():
            with self._settings_path.open("r", encoding="utf-8") as handle:
                data.update(json.load(handle))

        env_payload = {
            "openrouter_api_key": os.getenv("OPENROUTER_API_KEY", ""),
            "openrouter_model": os.getenv("OPENROUTER_MODEL", ""),
            "notifications_enabled": os.getenv("NUKHBAPROMPT_NOTIFICATIONS", ""),
        }
        for key, value in env_payload.items():
            if value not in {"", None}:
                data[key] = value

        optimize_shortcut = os.getenv("NUKHBAPROMPT_SHORTCUT", "").strip()
        if optimize_shortcut:
            shortcuts = DEFAULT_SHORTCUTS.copy() | dict(data.get("shortcuts", {}))
            shortcuts["optimize"] = optimize_shortcut
            data["shortcuts"] = shortcuts

        settings = AppSettings.from_dict(data)
        settings.validate()
        return settings

    def save_settings(self, settings: AppSettings) -> AppSettings:
        settings.validate()
        self._config_dir.mkdir(parents=True, exist_ok=True)
        with self._settings_path.open("w", encoding="utf-8") as handle:
            json.dump(settings.to_dict(), handle, indent=2)
        return settings
