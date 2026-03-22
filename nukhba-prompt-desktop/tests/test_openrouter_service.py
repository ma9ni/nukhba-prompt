from __future__ import annotations

from unittest.mock import Mock, patch

import requests

from nukhba_prompt_desktop.services.openrouter_service import OpenRouterService
from nukhba_prompt_desktop.services.storage_service import AppSettings
from nukhba_prompt_desktop.utils.errors import ProviderError


def test_optimize_raises_actionable_message_for_user_not_found():
    service = OpenRouterService()
    settings = AppSettings(openrouter_api_key="sk-or-v1-test", openrouter_model="demo/model")
    response = Mock()
    response.ok = False
    response.status_code = 401
    response.json.return_value = {"error": {"message": "User not found.", "code": 401}}
    response.text = '{"error":{"message":"User not found.","code":401}}'

    with patch.object(requests, "post", return_value=response):
        try:
            service.optimize(settings, [{"role": "user", "content": "hello"}])
        except ProviderError as exc:
            assert str(exc) == (
                "OpenRouter authentication failed: the API key was rejected "
                "(401 User not found). Check that OPENROUTER_API_KEY belongs "
                "to an active OpenRouter account."
            )
        else:  # pragma: no cover
            raise AssertionError("ProviderError was not raised")


def test_optimize_keeps_generic_provider_message_for_other_errors():
    service = OpenRouterService()
    settings = AppSettings(openrouter_api_key="sk-or-v1-test", openrouter_model="demo/model")
    response = Mock()
    response.ok = False
    response.status_code = 400
    response.json.return_value = {"error": {"message": "Bad request"}}
    response.text = '{"error":{"message":"Bad request"}}'

    with patch.object(requests, "post", return_value=response):
        try:
            service.optimize(settings, [{"role": "user", "content": "hello"}])
        except ProviderError as exc:
            assert str(exc) == "OpenRouter error: Bad request"
        else:  # pragma: no cover
            raise AssertionError("ProviderError was not raised")
