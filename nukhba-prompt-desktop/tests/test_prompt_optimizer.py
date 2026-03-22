from nukhba_prompt_desktop.services.storage_service import AppSettings
from nukhba_prompt_desktop.services.prompt_optimizer import PromptOptimizerService


def test_build_messages_includes_system_and_user_content():
    settings = AppSettings(system_prompt="system")
    messages = PromptOptimizerService.build_messages("hello", settings)
    assert messages[0] == {"role": "system", "content": "system"}
    assert messages[1]["role"] == "user"
    assert "Requested action: optimize." in messages[1]["content"]
    assert "Source text:\nhello" in messages[1]["content"]


def test_build_messages_includes_enhanced_structure_requirements():
    settings = AppSettings(system_prompt="system")
    messages = PromptOptimizerService.build_messages("build me a better prompt", settings, "enhanced")
    assert "Requested action: enhanced." in messages[1]["content"]
    assert "ROLE" in messages[1]["content"]
    assert "OBJECTIF" in messages[1]["content"]
    assert "FORMAT DE SORTIE" in messages[1]["content"]


def test_normalize_response_strips_code_fence_and_quotes():
    content = '```text\n"Refined prompt"\n```'
    assert PromptOptimizerService.normalize_response(content) == "Refined prompt"
