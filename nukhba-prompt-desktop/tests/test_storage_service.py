from nukhba_prompt_desktop.services.storage_service import (
    AppSettings,
    DEFAULT_SHORTCUTS,
    StorageService,
)


def test_storage_round_trip(tmp_path):
    service = StorageService(base_dir=tmp_path)
    saved = service.save_settings(
        AppSettings(
            openrouter_api_key="test-key",
            openrouter_model="demo/model",
            system_prompt="prompt",
            shortcuts=DEFAULT_SHORTCUTS.copy(),
            notifications_enabled=False,
        )
    )

    loaded = service.load_settings()

    assert loaded.openrouter_api_key == saved.openrouter_api_key
    assert loaded.openrouter_model == "demo/model"
    assert loaded.notifications_enabled is False
    assert loaded.shortcuts == DEFAULT_SHORTCUTS


def test_load_settings_migrates_legacy_default_shortcuts(tmp_path):
    service = StorageService(base_dir=tmp_path)
    service.settings_path.write_text(
        """
        {
          "shortcuts": {
            "optimize": "Ctrl+Shift+O",
            "summarize": "Ctrl+Shift+S",
            "translate": "Ctrl+Shift+T",
            "reply": "Ctrl+Shift+R",
            "grammar": "Ctrl+Shift+G"
          }
        }
        """.strip(),
        encoding="utf-8",
    )

    loaded = service.load_settings()

    assert loaded.shortcuts == DEFAULT_SHORTCUTS


def test_load_settings_preserves_custom_shortcut(tmp_path):
    service = StorageService(base_dir=tmp_path)
    service.settings_path.write_text(
        """
        {
          "shortcuts": {
            "optimize": "Ctrl+Alt+9"
          }
        }
        """.strip(),
        encoding="utf-8",
    )

    loaded = service.load_settings()

    assert loaded.shortcuts["optimize"] == "Ctrl+Alt+9"
    assert loaded.shortcuts["enhanced"] == DEFAULT_SHORTCUTS["enhanced"]
