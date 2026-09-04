from __future__ import annotations

from functools import lru_cache
from pathlib import Path


class FilePromptRepository:
    def __init__(self, base_path: Path | None = None):
        self.base_path = base_path or (
            Path(__file__).resolve().parents[2] / "resources" / "prompts"
        )

    @lru_cache(maxsize=None)
    def get(self, prompt_name: str) -> str:
        path = self.base_path / f"{prompt_name}.md"
        if not path.is_file():
            raise FileNotFoundError(f"No existe el prompt: {path}")
        return path.read_text(encoding="utf-8").strip()
