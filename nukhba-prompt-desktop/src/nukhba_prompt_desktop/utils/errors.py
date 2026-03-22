class NukhbaPromptError(Exception):
    """Base application error."""


class ClipboardError(NukhbaPromptError):
    """Raised when clipboard input or output is invalid."""


class ConfigurationError(NukhbaPromptError):
    """Raised when application settings are incomplete or invalid."""


class ProviderError(NukhbaPromptError):
    """Raised when OpenRouter fails or returns an invalid payload."""


class ShortcutRegistrationError(NukhbaPromptError):
    """Raised when the global shortcut cannot be registered."""
