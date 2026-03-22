from nukhba_prompt_desktop.services.storage_service import AppSettings, StorageService


def test_storage_round_trip(tmp_path):
    service = StorageService(base_dir=tmp_path)
    saved = service.save_settings(
        AppSettings(
            openrouter_api_key="test-key",
            openrouter_model="demo/model",
            system_prompt="prompt",
            shortcut="Ctrl+Shift+O",
            notifications_enabled=False,
        )
    )

    loaded = service.load_settings()

    assert loaded.openrouter_api_key == saved.openrouter_api_key
    assert loaded.openrouter_model == "demo/model"
    assert loaded.notifications_enabled is False
