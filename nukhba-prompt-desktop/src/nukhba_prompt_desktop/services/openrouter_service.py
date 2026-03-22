from __future__ import annotations

import requests

from nukhba_prompt_desktop.services.storage_service import AppSettings
from nukhba_prompt_desktop.utils.errors import ConfigurationError, ProviderError


class OpenRouterService:
    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, timeout_seconds: int = 30) -> None:
        self.timeout_seconds = timeout_seconds

    def optimize(self, settings: AppSettings, messages: list[dict[str, str]]) -> str:
        if not settings.openrouter_api_key.strip():
            raise ConfigurationError("OpenRouter API key is missing.")

        try:
            response = requests.post(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/ma9ni/nukhba-prompt",
                    "X-Title": "NukhbaPrompt Desktop",
                },
                json={
                    "model": settings.openrouter_model,
                    "messages": messages,
                    "temperature": 0.3,
                },
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            raise ProviderError(f"OpenRouter request failed: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise ProviderError("OpenRouter returned invalid JSON.") from exc

        if not response.ok:
            error_message = payload.get("error", {}).get("message") or response.text
            raise ProviderError(
                self._build_error_message(response.status_code, str(error_message))
            )

        try:
            content = payload["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("OpenRouter returned an unexpected response format.") from exc

        if not isinstance(content, str) or not content.strip():
            raise ProviderError("OpenRouter returned empty optimization text.")
        return content

    @staticmethod
    def _build_error_message(status_code: int, error_message: str) -> str:
        normalized_message = error_message.strip()
        if status_code == 401 and normalized_message.lower() == "user not found.":
            return (
                "OpenRouter authentication failed: the API key was rejected "
                "(401 User not found). Check that OPENROUTER_API_KEY belongs "
                "to an active OpenRouter account."
            )
        return f"OpenRouter error: {normalized_message}"
