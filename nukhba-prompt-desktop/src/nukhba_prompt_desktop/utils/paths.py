from __future__ import annotations

import os
import platform
from pathlib import Path


def get_app_data_dir(app_name: str = "nukhba_prompt_desktop") -> Path:
    system = platform.system()

    if system == "Windows":
        base = os.getenv("APPDATA") or os.getenv("LOCALAPPDATA")
        if base:
            return Path(base) / app_name
    elif system == "Darwin":
        return Path.home() / "Library" / "Application Support" / app_name

    return Path.home() / ".config" / app_name
