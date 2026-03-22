from __future__ import annotations


class PromptOptimizerService:
    @staticmethod
    def build_messages(source_text: str, system_prompt: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": source_text},
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
