from nukhba_prompt_desktop.services.prompt_optimizer import PromptOptimizerService


def test_build_messages_includes_system_and_user_content():
    messages = PromptOptimizerService.build_messages("hello", "system")
    assert messages == [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "hello"},
    ]


def test_normalize_response_strips_code_fence_and_quotes():
    content = '```text\n"Refined prompt"\n```'
    assert PromptOptimizerService.normalize_response(content) == "Refined prompt"
