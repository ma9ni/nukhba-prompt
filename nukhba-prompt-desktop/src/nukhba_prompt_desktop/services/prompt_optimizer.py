from __future__ import annotations

from nukhba_prompt_desktop.services.storage_service import AppSettings

class PromptOptimizerService:
    @staticmethod
    def build_messages(
        source_text: str, settings: AppSettings, action: str = "optimize"
    ) -> list[dict[str, str]]:
        action_instructions = {
            "optimize": "Rewrite the text to make it clearer, sharper, and more effective.",
            "summarize": "Summarize the text into a concise and useful version.",
            "translate": "Translate the text while preserving intent and tone.",
            "reply": "Write a professional reply based on the text.",
            "grammar": "Fix grammar, spelling, punctuation, and clarity without changing the meaning.",
        }

        context_parts = []
        if settings.profile_role.strip():
            context_parts.append(f"User role: {settings.profile_role.strip()}")
        if settings.profile_domains.strip():
            context_parts.append(f"Domains: {settings.profile_domains.strip()}")
        if settings.preferred_language.strip():
            context_parts.append(f"Preferred language: {settings.preferred_language.strip()}")
        if settings.writing_preferences.strip():
            context_parts.append(f"Writing preferences: {settings.writing_preferences.strip()}")
        if settings.additional_context.strip():
            context_parts.append(f"Additional context: {settings.additional_context.strip()}")
        if settings.rules_text.strip():
            context_parts.append(f"User rules: {settings.rules_text.strip()}")

        user_message = "\n\n".join(
            part
            for part in [
                f"Requested action: {action}.",
                action_instructions.get(action, action_instructions["optimize"]),
                "\n".join(context_parts).strip(),
                f"Source text:\n{source_text}",
            ]
            if part
        )

        return [
            {"role": "system", "content": settings.system_prompt},
            {"role": "user", "content": user_message},
        ]

    @staticmethod
    def normalize_response(content: str) -> str:
        text = (content or "").strip()

        if text.startswith("```") and text.endswith("```"):
            first_newline = text.find("\n")
            if first_newline != -1:
                text = text[first_newline + 1 :]
            text = text[:-3].strip()

        if (text.startswith('"') and text.endswith('"')) or (
            text.startswith("'") and text.endswith("'")
        ):
            text = text[1:-1].strip()

        return text
